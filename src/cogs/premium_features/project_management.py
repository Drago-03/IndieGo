import discord
from discord.ext import commands
from typing import Optional
import json
import os

class ProjectManagement(commands.Cog):
    """
    Project management and scaffolding features
    """
    def __init__(self, bot):
        self.bot = bot
        
        # Load project templates
        with open('src/config/project_templates.json', 'r') as f:
            self.templates = json.load(f)

    @commands.command()
    async def create_project(self, ctx, name: str, template: str):
        """
        Create a new project structure
        
        Args:
            ctx: Command context
            name (str): Project name
            template (str): Template to use
        """
        if template not in self.templates:
            templates_list = "\n".join(f"• {t}" for t in self.templates.keys())
            await ctx.send(f"Invalid template. Available templates:\n{templates_list}")
            return

        # Generate project structure
        structure = self._generate_structure(name, template)
        
        # Create embed with project structure
        embed = discord.Embed(
            title=f"Project Structure: {name}",
            description="Here's your project structure:",
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="Directory Structure",
            value=f"```\n{structure}\n```",
            inline=False
        )
        
        # Add setup instructions
        embed.add_field(
            name="Setup Instructions",
            value=self.templates[template]["setup_instructions"],
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def estimate(self, ctx, *, requirements: str):
        """
        Estimate project complexity and time
        
        Args:
            ctx: Command context
            requirements (str): Project requirements
        """
        # Analyze requirements and generate estimate
        analysis = self._analyze_requirements(requirements)
        
        embed = discord.Embed(
            title="Project Estimation",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Complexity Score",
            value=f"{analysis['complexity']}/10",
            inline=True
        )
        
        embed.add_field(
            name="Estimated Time",
            value=analysis['time_estimate'],
            inline=True
        )
        
        embed.add_field(
            name="Team Size",
            value=analysis['recommended_team_size'],
            inline=True
        )
        
        embed.add_field(
            name="Key Considerations",
            value="\n".join(f"• {c}" for c in analysis['considerations']),
            inline=False
        )

        await ctx.send(embed=embed)

    def _generate_structure(self, name: str, template: str) -> str:
        """
        Generate project structure based on template
        
        Args:
            name (str): Project name
            template (str): Template name
            
        Returns:
            str: Formatted project structure
        """
        structure = []
        base = self.templates[template]["structure"]
        
        def build_tree(items, prefix=""):
            for item in items:
                if isinstance(item, dict):
                    for dirname, contents in item.items():
                        structure.append(f"{prefix}└── {dirname}/")
                        build_tree(contents, prefix + "    ")
                else:
                    structure.append(f"{prefix}└── {item}")
        
        structure.append(f"{name}/")
        build_tree(base, "    ")
        
        return "\n".join(structure)

    def _analyze_requirements(self, requirements: str) -> dict:
        """
        Analyze project requirements
        
        Args:
            requirements (str): Project requirements
            
        Returns:
            dict: Analysis results
        """
        # This is a simplified analysis
        words = requirements.split()
        complexity = min(len(words) // 20, 10)  # Simple complexity metric
        
        considerations = [
            "Ensure proper documentation",
            "Plan for scalability",
            "Consider security implications",
            "Include automated testing"
        ]
        
        if complexity > 7:
            considerations.extend([
                "Consider microservices architecture",
                "Plan for load balancing",
                "Implement monitoring system"
            ])
        
        return {
            "complexity": complexity,
            "time_estimate": f"{complexity * 2} weeks",
            "recommended_team_size": f"{max(1, complexity // 3)}-{max(2, complexity // 2)} developers",
            "considerations": considerations
        }

async def setup(bot):
    await bot.add_cog(ProjectManagement(bot))