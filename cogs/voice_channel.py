import discord
from discord.ext import commands
import os
import asyncio
from discord import app_commands
from gtts import gTTS
import tempfile
import wave
import pyaudio
from google.cloud import speech_v1
from datetime import datetime

class VoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recording = False
        self.speech_client = speech_v1.SpeechClient()
        self.voice_states = {}

    async def ensure_voice(self, ctx):
        """Ensure bot is in voice channel"""
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel first!")
            return False
        return True

    @commands.command(name="join")
    async def join_command(self, ctx):
        """Join a voice channel"""
        if await self.ensure_voice(ctx):
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()
            await ctx.send(f"Joined {channel.name}")

    @app_commands.command(name="join", description="Join a voice channel")
    async def join_slash(self, interaction: discord.Interaction):
        """Join a voice channel"""
        if not interaction.user.voice:
            await interaction.response.send_message("You need to be in a voice channel first!", ephemeral=True)
            return
        
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.move_to(channel)
        else:
            await channel.connect()
        await interaction.response.send_message(f"Joined {channel.name}", ephemeral=True)

    @commands.command(name="leave")
    async def leave_command(self, ctx):
        """Leave the voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel")
        else:
            await ctx.send("I'm not in a voice channel")

    @app_commands.command(name="leave", description="Leave the voice channel")
    async def leave_slash(self, interaction: discord.Interaction):
        """Leave the voice channel"""
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Left the voice channel", ephemeral=True)
        else:
            await interaction.response.send_message("I'm not in a voice channel", ephemeral=True)

    @commands.command(name="record")
    async def record_command(self, ctx, duration: int = 30):
        """Record voice for specified duration (default 30s)"""
        if not ctx.voice_client:
            await ctx.send("I need to be in a voice channel first!")
            return

        if self.recording:
            await ctx.send("Already recording!")
            return

        self.recording = True
        await ctx.send(f"🎙️ Recording for {duration} seconds...")

        # Setup recording
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

        frames = []
        
        try:
            for i in range(0, int(RATE / CHUNK * duration)):
                if not self.recording:
                    break
                data = stream.read(CHUNK)
                frames.append(data)

            # Stop and close stream
            stream.stop_stream()
            stream.close()
            p.terminate()

            # Save recording
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            await ctx.send("📝 Converting speech to text...")

            # Transcribe
            with open(filename, 'rb') as audio_file:
                content = audio_file.read()

            audio = speech_v1.RecognitionAudio(content=content)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code="en-US",
            )

            response = self.speech_client.recognize(config=config, audio=audio)
            transcript = ""
            
            for result in response.results:
                transcript += result.alternatives[0].transcript + "\n"

            # Send transcript
            await ctx.send(f"🔤 Transcript:\n```{transcript}```")
            
            # Cleanup
            os.remove(filename)

        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")
        finally:
            self.recording = False

    @app_commands.command(name="record", description="Record voice and convert to text")
    async def record_slash(self, interaction: discord.Interaction, duration: int = 30):
        """Record voice for specified duration"""
        if not interaction.guild.voice_client:
            await interaction.response.send_message("I need to be in a voice channel first!", ephemeral=True)
            return

        if self.recording:
            await interaction.response.send_message("Already recording!", ephemeral=True)
            return

        await interaction.response.send_message(f"🎙️ Recording for {duration} seconds...", ephemeral=True)
        
        # Same recording logic as above but with interaction responses
        # ...implement similar recording logic with interaction.followup.send()...

    @commands.command(name="play")
    async def play_command(self, ctx, url: str):
        """Play audio from URL"""
        if not ctx.voice_client:
            if not await self.ensure_voice(ctx):
                return
            await ctx.author.voice.channel.connect()

        try:
            ctx.voice_client.stop()
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
            ctx.voice_client.play(source)
            await ctx.send(f"🎵 Now playing: {url}")
        except Exception as e:
            await ctx.send(f"❌ Error playing audio: {str(e)}")

    @app_commands.command(name="play", description="Play audio from URL")
    async def play_slash(self, interaction: discord.Interaction, url: str):
        """Play audio from URL"""
        if not interaction.guild.voice_client:
            if not interaction.user.voice:
                await interaction.response.send_message("You need to be in a voice channel first!", ephemeral=True)
                return
            await interaction.user.voice.channel.connect()

        try:
            interaction.guild.voice_client.stop()
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
            interaction.guild.voice_client.play(source)
            await interaction.response.send_message(f"🎵 Now playing: {url}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error playing audio: {str(e)}", ephemeral=True)

    @commands.command(name="tts")
    async def tts_command(self, ctx, *, text: str):
        """Convert text to speech and play it"""
        if not ctx.voice_client:
            if not await self.ensure_voice(ctx):
                return
            await ctx.author.voice.channel.connect()

        try:
            # Create temporary file for TTS audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts = gTTS(text=text, lang='en')
                tts.save(fp.name)
                
                ctx.voice_client.stop()
                source = discord.FFmpegPCMAudio(fp.name)
                ctx.voice_client.play(source, after=lambda e: os.remove(fp.name))
                
            await ctx.send("🗣️ Playing TTS message")
        except Exception as e:
            await ctx.send(f"❌ Error with TTS: {str(e)}")

    @app_commands.command(name="tts", description="Convert text to speech and play it")
    async def tts_slash(self, interaction: discord.Interaction, text: str):
        """Convert text to speech and play it"""
        if not interaction.guild.voice_client:
            if not interaction.user.voice:
                await interaction.response.send_message("You need to be in a voice channel first!", ephemeral=True)
                return
            await interaction.user.voice.channel.connect()

        try:
            # Create temporary file for TTS audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                tts = gTTS(text=text, lang='en')
                tts.save(fp.name)
                
                interaction.guild.voice_client.stop()
                source = discord.FFmpegPCMAudio(fp.name)
                interaction.guild.voice_client.play(source, after=lambda e: os.remove(fp.name))
                
            await interaction.response.send_message("🗣️ Playing TTS message", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error with TTS: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(VoiceChannel(bot))