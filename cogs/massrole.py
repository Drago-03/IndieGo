import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import pandas as pd  # For reading Excel files
import PyPDF2  # For reading PDF files
import os
import logging

logger = logging.getLogger('IndieGOBot')

class MassRole(commands.Cog):
    """Cog for mass role assignment from files"""
    
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Mass Role Assignment',
            callback=self.context_massrole,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def process_file(self, interaction, attachment, role):
        """Process the uploaded file and assign roles"""
        file_name = attachment.filename.lower()
        file_content = await attachment.read()
        user_list = []
        
        try:
            if file_name.endswith(".xlsx"):
                with open("temp.xlsx", "wb") as f:
                    f.write(file_content)
                df = pd.read_excel("temp.xlsx", header=None)
                user_list = df[0].astype(str).tolist()
                os.remove("temp.xlsx")
            
            elif file_name.endswith(".pdf"):
                with open("temp.pdf", "wb") as f:
                    f.write(file_content)
                with open("temp.pdf", "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        user_list.extend(page.extract_text().splitlines())
                os.remove("temp.pdf")
            else:
                await interaction.followup.send("Unsupported file format. Please upload an Excel or PDF file.", ephemeral=True)
                return
            
            count = 0
            not_found = []
            permission_errors = []
            
            # Send initial response
            await interaction.followup.send("Processing role assignments... Please wait.", ephemeral=True)
            
            for user_info in user_list:
                user_info = user_info.strip()
                if not user_info:
                    continue
                
                try:
                    user = interaction.guild.get_member_named(user_info)
                    if user is None and user_info.isdigit():
                        user = interaction.guild.get_member(int(user_info))
                    
                    if user is None:
                        not_found.append(user_info)
                        continue
                    
                    await user.add_roles(role)
                    count += 1
                    await asyncio.sleep(0.5)  # Rate limiting to avoid API issues
                    
                except discord.Forbidden:
                    permission_errors.append(user_info)
                    logger.error(f"Permission error while assigning role to {user_info}")
                except discord.HTTPException as e:
                    logger.error(f"HTTP error while assigning role to {user_info}: {str(e)}")
                    await interaction.followup.send(f"Error assigning role to {user_info}: {str(e)}", ephemeral=True)
            
            # Send summary
            response = f"✅ Role assigned to {count} users successfully.\n"
            if not_found:
                response += f"\n❌ Users not found ({len(not_found)}):\n" + "\n".join(not_found[:10])
                if len(not_found) > 10:
                    response += f"\n...and {len(not_found) - 10} more"
            if permission_errors:
                response += f"\n⚠️ Permission errors ({len(permission_errors)}):\n" + "\n".join(permission_errors[:10])
                if len(permission_errors) > 10:
                    response += f"\n...and {len(permission_errors) - 10} more"
            
            await interaction.followup.send(response, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error in mass role assignment: {str(e)}")
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)
        finally:
            # Ensure temporary files are cleaned up
            if os.path.exists("temp.xlsx"):
                os.remove("temp.xlsx")
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")

    @commands.hybrid_command(
        name="massrole",
        description="Assign a role to multiple users from an Excel or PDF file"
    )
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(
        role="The role to assign to users"
    )
    async def massrole(self, ctx: commands.Context, role: discord.Role):
        """
        Assign a role to multiple users from an Excel or PDF file
        
        Parameters:
        -----------
        role: The role to assign to the users
        Attachment: An Excel (.xlsx) or PDF file containing usernames or user IDs
        """
        if not ctx.interaction:
            # Handle prefix command
            if not ctx.message.attachments:
                await ctx.send("Please upload an Excel (.xlsx) or PDF file containing usernames or user IDs.")
                return
            await self.process_file(ctx, ctx.message.attachments[0], role)
        else:
            # Handle slash command
            await ctx.interaction.response.send_message(
                "Please upload the Excel (.xlsx) or PDF file containing usernames or user IDs.",
                ephemeral=True
            )

    @app_commands.command(
        name="massrole_upload",
        description="Upload a file to assign roles to multiple users"
    )
    @app_commands.describe(
        role="The role to assign to users",
        file="Excel (.xlsx) or PDF file containing usernames or user IDs"
    )
    async def massrole_upload(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        file: discord.Attachment
    ):
        """Slash command version of massrole with file upload"""
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You don't have permission to manage roles!", ephemeral=True)
            return
            
        await interaction.response.defer(ephemeral=True)
        await self.process_file(interaction, file, role)

    async def context_massrole(self, interaction: discord.Interaction, message: discord.Message):
        """Context menu version of massrole"""
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You don't have permission to manage roles!", ephemeral=True)
            return
            
        if not message.attachments:
            await interaction.response.send_message("No file found in this message!", ephemeral=True)
            return
            
        await interaction.response.send_message(
            "Please select the role to assign:",
            ephemeral=True,
            view=RoleSelectionView(self.bot, message.attachments[0])
        )

class RoleSelectionView(discord.ui.View):
    def __init__(self, bot, attachment):
        super().__init__()
        self.bot = bot
        self.attachment = attachment

    @discord.ui.select(
        cls=discord.ui.RoleSelect,
        placeholder="Select a role to assign",
        min_values=1,
        max_values=1,
    )
    async def select_role(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        cog = self.bot.get_cog('MassRole')
        if cog:
            await interaction.response.defer(ephemeral=True)
            await cog.process_file(interaction, self.attachment, select.values[0])
        else:
            await interaction.response.send_message("Something went wrong. Please try again.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MassRole(bot))