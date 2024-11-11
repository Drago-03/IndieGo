import discord
from discord.ext import commands
from typing import Optional
from models.code_analysis import CodeAnalyzer
from models.subscription import Subscription

class CodeReview(commands.Cog):
    """
    Advanced code review and analysis features
    """
    def __init__(self, bot):
        self.bot = bot
        self.analyzer = CodeAnalyzer()
        self.subscription = Subscription()

    @commands.command()
    async def review(self, ctx, *, code: str):
        """
        Perform comprehensive code review
        
        Args:
            ctx: Command context
            code (str): Code to review
        """
        # Check subscription status
        sub = await self.subscription.get_subscription(ctx.author.id)
        is_premium = sub and sub['tier'] in ['pro', 'enterprise']

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

        # Premium features
        if is_premium:
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
        else:
            embed.add_field(
                name="🌟 Premium Features Available",
                value="Upgrade to Pro for detailed suggestions, performance tips, and best practices!",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def optimize(self, ctx, *, code: str):
        """
        Suggest code optimizations (Premium only)
        
        Args:
            ctx: Command context
            code (str): Code to optimize
        """
        sub = await self.subscription.get_subscription(ctx.author.id)
        if not sub or sub['tier'] not in ['pro', 'enterprise']:
            await ctx.send("⭐ This is a premium feature. Upgrade to Pro or Enterprise to access code optimization!")
            return

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