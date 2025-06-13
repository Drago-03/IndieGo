import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View
from config import SUPPORT_SERVER_LINK

class HelpDropdown(Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="General", description="General bot commands", emoji="🤖"),
            discord.SelectOption(label="Moderation", description="Moderation commands", emoji="🛡️"),
            discord.SelectOption(label="Fun", description="Fun commands", emoji="🎮"),
            discord.SelectOption(label="AI Assistant", description="AI-powered commands", emoji="🧠"),
            discord.SelectOption(label="Coding", description="Programming help commands", emoji="💻"),
            discord.SelectOption(label="Reddit", description="Reddit commands", emoji="🔗"),
            discord.SelectOption(label="AutoMod", description="AutoMod commands", emoji="🔒"),
            discord.SelectOption(label="DM Interaction", description="DM interaction commands", emoji="✉️"),
            discord.SelectOption(label="Logging", description="Logging commands", emoji="📜"),
            discord.SelectOption(label="Tickets", description="Ticketing commands", emoji="🎫"),
            discord.SelectOption(label="Voice", description="Voice channel commands", emoji="🔊"),
            discord.SelectOption(label="OCR", description="OCR commands", emoji="📄"),
            discord.SelectOption(label="Chat", description="Natural chat interactions", emoji="💬")
        ]
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(
            title=f"{category} Commands", 
            description=f"Here are the commands for {category}:", 
            color=discord.Color.blue()
        )
        
        if category == "General":
            embed.add_field(name="Commands", value="• ping - Check bot latency\n• about - About the bot\n• choose - Choose between options\n• serverinfo - Server information\n• support - Get support server link\n• profile - Show profile options", inline=False)
        elif category == "Moderation":
            embed.add_field(name="Commands", value="• kick - Kick a member\n• ban - Ban a member\n• mute - Mute a member\n• unmute - Unmute a member\n• warn - Warn a member\n• clear - Clear messages\n• massrole - Assign role to all members or from a file\n• autorole_add - Add a role to auto-assign to new members\n• autorole_remove - Remove a role from auto-assignment\n• autorole_list - List all auto-assigned roles\n• autorole_clear - Clear all auto-assigned roles\n• setup - Setup all moderation features", inline=False)
            embed.add_field(name="About Setup", value="The setup command configures all moderation features:\n• Creates and configures Quarantine role\n• Creates and configures Muted role with proper permissions\n• Sets up mod-logs channel with proper permissions\n• Initializes AutoMod with default settings\n• Shows real-time progress of setup\n• Requires Administrator permission", inline=False)
            embed.add_field(name="About Autoroles", value="Autoroles automatically assign roles to new members when they join:\n• Use autorole_add to set up automatic role assignment\n• Roles will be given instantly when members join\n• Multiple roles can be configured\n• All actions are logged in mod-logs\n• Requires 'Manage Roles' permission", inline=False)
            embed.add_field(name="About Bot Roles", value="Bot roles are automatically managed:\n• Creates a 'Bot' role if it doesn't exist\n• Automatically assigns the role to all bots\n• Removes human autoroles from bots\n• Runs automatically when bot joins server\n• Can be manually triggered with setup_bot_roles\n• Requires Administrator permission", inline=False)
            embed.add_field(name="About Massrole", value="Massrole command has two modes:\n• Default: Assigns role to all server members\n• With file: Assigns role only to users listed in the file (Excel/PDF)\n• Automatically skips users who already have the role\n• Shows real-time progress updates\n• Provides detailed summary when complete\n• Requires 'Manage Roles' permission", inline=False)
        elif category == "Fun":
            embed.add_field(name="Commands", value="• roll - Roll a dice\n• 8ball - Ask the magic 8ball\n• joke - Get a random joke\n• codechallenge - Get a coding challenge\n• trivia - Start a programming trivia", inline=False)
        elif category == "AI Assistant":
            embed.add_field(name="Commands", value="• ask - Ask the AI a question\n• codehelp - Get coding help\n• explain - Get code explanation", inline=False)
        elif category == "Coding":
            embed.add_field(name="Commands", value="• debug - Debug your code\n• optimize - Optimize your code\n• format - Format your code", inline=False)
        elif category == "Reddit":
            embed.add_field(name="Commands", value="• meme - Fetch a programming meme", inline=False)
        elif category == "AutoMod":
            embed.add_field(name="Commands", value="• automod_setup - Setup AutoMod\n• add_filter - Add word filter\n• remove_filter - Remove word filter", inline=False)
        elif category == "DM Interaction":
            embed.add_field(name="Commands", value="• dm - Send a DM\n• reply - Reply to a DM", inline=False)
        elif category == "Logging":
            embed.add_field(name="Commands", value="• setup_logs - Setup logging channels\n• view_logs - View recent logs", inline=False)
        elif category == "Tickets":
            embed.add_field(name="Commands", value="• ticket - Create a ticket\n• setup_tickets - Setup ticket system\n• close - Close a ticket", inline=False)
        elif category == "Voice":
            embed.add_field(name="Commands", value="• join - Join a voice channel\n• leave - Leave voice channel\n• play - Play music", inline=False)
        elif category == "OCR":
            embed.add_field(name="Commands", value="• scan - Scan image for text\n• extract - Extract text from image", inline=False)
        elif category == "Chat":
            embed.add_field(name="Commands", value="• enable_chat - Enable natural chat in a channel\n• disable_chat - Disable natural chat in a channel\n\nIn enabled channels, you can:\n• Mention @IndieGO\n• Reply to IndieGO's messages\n• Include 'indiego' in your message", inline=False)
            embed.add_field(name="About Chat", value="IndieGO acts as a friendly mentor and peer, helping students with:\n• Programming questions\n• Design discussions\n• Learning resources\n• Project guidance\n• Technical concepts\n• Career advice", inline=False)

        embed.set_footer(text="Use . before commands (e.g. .help) or use slash commands")
        
        try:
            if interaction.response.is_done():
                await interaction.message.edit(embed=embed, view=self.view)
            else:
                await interaction.response.edit_message(embed=embed, view=self.view)
        except discord.errors.InteractionNotResponded:
            await interaction.response.send_message(embed=embed, view=self.view)
        except Exception as e:
            logger.error(f"Error in help dropdown: {str(e)}")
            try:
                await interaction.followup.send(embed=embed, view=self.view)
            except:
                if interaction.message:
                    await interaction.message.edit(embed=embed, view=self.view)

class HelpView(View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.add_item(HelpDropdown(bot))

    async def on_timeout(self):
        """Disable the view when it times out"""
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(view=self)
        except:
            pass

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Show help information with a dropdown menu"""
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Select a category from the dropdown menu below to see available commands.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Prefix Commands", value="Use i! before commands (e.g. i!help)", inline=False)
        embed.add_field(name="Slash Commands", value="Use / to access slash commands", inline=False)
        embed.set_footer(text="Select a category below to view specific commands")
        
        view = HelpView(self.bot)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

    @app_commands.command(name="help", description="Show help information with a dropdown menu")
    async def help_slash(self, interaction: discord.Interaction):
        """Show help information with a dropdown menu"""
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Select a category from the dropdown menu below to see available commands.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Prefix Commands", value="Use i! before commands (e.g. i!help)", inline=False)
        embed.add_field(name="Slash Commands", value="Use / to access slash commands", inline=False)
        embed.set_footer(text="Select a category below to view specific commands")
        
        view = HelpView(self.bot)
        message = await interaction.response.send_message(embed=embed, view=view)
        if isinstance(message, discord.InteractionMessage):
            view.message = message
        else:
            view.message = await interaction.original_response()

async def setup(bot):
    await bot.add_cog(Help(bot))