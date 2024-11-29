import discord
from discord.ext import commands
from typing import Optional
from models.code_analysis import CodeAnalyzer

class CodeReview(commands.Cog):
    """
    Advanced code review and analysis features
    """
    def __init__(self, bot):
        self.bot = bot
        self.analyzer = CodeAnalyzer()

    @commands.command()
    async def review(self, ctx, *, code: str):
        """
        Perform comprehensive code review
        
        Args:
            ctx: Command context
            code (str): Code to review
        """
        # Extract code from Discord code block if present
        code = code.strip('`').strip()
        if code.startswith('python\n'):
            code = code[7:]

        # Analyze code
        analysis = self.analyzer.analyze_code(code)

        # Create detailed embed
        embed = discord.Embed(
            title="Code Review Results",
            color=discord.Color.blue()
        )

        # Basic analysis for free users
        embed.add_field(
            name="Complexity Score",
            value=f"{analysis.complexity}/10 " + 
                  ("(High)" if analysis.complexity > 7 else 
                   "(Medium)" if analysis.complexity > 4 else "(Good)"),
            inline=False
        )

        if analysis.security_issues:
            embed.add_field(
                name="⚠️ Security Issues",
                value="\n".join(f"• {issue}" for issue in analysis.security_issues),
                inline=False
            )

        if analysis.best_practices:
            embed.add_field(
                name="Best Practices",
                value="\n".join(f"• {practice}" for practice in analysis.best_practices),
                inline=False
            )

        if analysis.performance_tips:
            embed.add_field(
                name="Performance Tips",
                value="\n".join(f"• {tip}" for tip in analysis.performance_tips),
                inline=False
            )

        if analysis.suggestions:
            embed.add_field(
                name="Suggestions",
                value="\n".join(f"• {suggestion}" for suggestion in analysis.suggestions),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def optimize(self, ctx, *, code: str):
        """
        Suggest code optimizations
        
        Args:
            ctx: Command context
            code (str): Code to optimize
        """
        # Code optimization logic here
        analysis = self.analyzer.analyze_code(code)
        
        embed = discord.Embed(
            title="Code Optimization Suggestions",
            color=discord.Color.green()
        )

        if analysis.performance_tips:
            embed.add_field(
                name="Performance Improvements",
                value="\n".join(f"• {tip}" for tip in analysis.performance_tips),
                inline=False
            )
        else:
            embed.add_field(
                name="Analysis Result",
                value="No obvious optimization opportunities found. Your code looks efficient!",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CodeReview(bot))