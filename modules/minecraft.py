import discord
import random
from discord.ext import commands
from urllib.parse import quote


class Minecraft:
    """Minecraft-related commands"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/iT7Gpdo.png"

    @commands.command()
    async def skin(self, ctx, *, player: str):
        """Show skin of a Minecraft player"""
        await ctx.send(
            embed=discord.Embed(
                color=random.randint(0x000000, 0xFFFFFF),
                timestamp=ctx.message.created_at,
            )
            .add_field(
                name=f"**{player if len(player) < 15 else f'{player[:5]}...'}**",
                value=chr(173),
            )
            .set_image(url=f"https://mc-heads.net/body/{quote(player)}")
            .set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        )


def setup(bot):
    bot.add_cog(Minecraft(bot))
