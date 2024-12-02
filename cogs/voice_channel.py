import discord
from discord.ext import commands
import os
import asyncio
from discord import app_commands
from gtts import gTTS
import tempfile
from pydub import AudioSegment
from google.cloud import speech

class VoiceChannel(commands.Cog):
    """Cog for voice channel features"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def join_command(self, ctx):
        """Join a voice channel"""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")

    @app_commands.command(name="join", description="Join a voice channel")
    async def join_slash(self, interaction: discord.Interaction):
        """Join a voice channel"""
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            await channel.connect()
            await interaction.response.send_message(f"Joined {channel.name}", ephemeral=True)
        else:
            await interaction.response.send_message("You are not connected to a voice channel.", ephemeral=True)

    @commands.command(name="leave")
    async def leave_command(self, ctx):
        """Leave a voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("I am not connected to a voice channel.")

    @app_commands.command(name="leave", description="Leave a voice channel")
    async def leave_slash(self, interaction: discord.Interaction):
        """Leave a voice channel"""
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Disconnected from the voice channel.", ephemeral=True)
        else:
            await interaction.response.send_message("I am not connected to a voice channel.", ephemeral=True)

    @commands.command(name="play")
    async def play_command(self, ctx, url: str):
        """Play a sound from a URL"""
        if ctx.voice_client:
            ctx.voice_client.stop()
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            ctx.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
        else:
            await ctx.send("I am not connected to a voice channel.")

    @app_commands.command(name="play", description="Play a sound from a URL")
    async def play_slash(self, interaction: discord.Interaction, url: str):
        """Play a sound from a URL"""
        if interaction.guild.voice_client:
            interaction.guild.voice_client.stop()
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            interaction.guild.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options))
            await interaction.response.send_message(f"Playing sound from {url}", ephemeral=True)
        else:
            await interaction.response.send_message("I am not connected to a voice channel.", ephemeral=True)

    @commands.command(name="record")
    async def record_command(self, ctx):
        """Record voice and convert to text"""
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Recording started...")

            # Placeholder for recording logic
            await asyncio.sleep(60)  # Simulate recording duration

            await ctx.send("Recording stopped. Converting to text...")

            # Placeholder for voice-to-text conversion logic
            text = "This is a sample transcription of the recorded audio."

            await ctx.author.send(f"Here is the transcription of your recording:\n{text}")
        else:
            await ctx.send("I am not connected to a voice channel.")

    @app_commands.command(name="record", description="Record voice and convert to text")
    async def record_slash(self, interaction: discord.Interaction):
        """Record voice and convert to text"""
        if interaction.guild.voice_client:
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Recording started...", ephemeral=True)

            # Placeholder for recording logic
            await asyncio.sleep(60)  # Simulate recording duration

            await interaction.followup.send("Recording stopped. Converting to text...", ephemeral=True)

            # Placeholder for voice-to-text conversion logic
            text = "This is a sample transcription of the recorded audio."

            await interaction.user.send(f"Here is the transcription of your recording:\n{text}")
        else:
            await interaction.response.send_message("I am not connected to a voice channel.", ephemeral=True)

    @commands.command(name="tts")
    async def tts_command(self, ctx, *, text: str):
        """Convert text to speech and play in voice channel"""
        if ctx.voice_client:
            tts = gTTS(text)
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tts.save(fp.name)
                ctx.voice_client.play(discord.FFmpegPCMAudio(fp.name))
        else:
            await ctx.send("I am not connected to a voice channel.")

    @app_commands.command(name="tts", description="Convert text to speech and play in voice channel")
    async def tts_slash(self, interaction: discord.Interaction, text: str):
        """Convert text to speech and play in voice channel"""
        if interaction.guild.voice_client:
            tts = gTTS(text)
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tts.save(fp.name)
                interaction.guild.voice_client.play(discord.FFmpegPCMAudio(fp.name))
            await interaction.response.send_message(f"Playing TTS: {text}", ephemeral=True)
        else:
            await interaction.response.send_message("I am not connected to a voice channel.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(VoiceChannel(bot))