import discord
import random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Space:
    """No one knows exactly how big space is..."""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/Dxyor6p.png"
        self.nasa_key = self.bot.config.nasa_key

    @commands.command()
    @commands.cooldown(1.0, 15.0, commands.BucketType.user)
    async def apod(self, ctx):
        """
        Shows Astronomy Picture of the Day.
        """

        async with ctx.typing():
            async with self.bot.session.get(
                f"https://api.nasa.gov/planetary/apod?api_key={self.nasa_key}"
            ) as resp:
                cont = await resp.json()

                embed = discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                    title="Astronomy Picture of the Day",
                    description=f'`{cont["title"]}` ● `{cont["date"]}`'
                    f'\n\n{cont["explanation"]}',
                )

                if not cont["url"].endswith(("gif", "png", "jpg")):
                    embed.add_field(
                        name="**🔴 Watch**", value=f"**[➢ Watch this!]({cont['url']})**"
                    )
                else:
                    embed.set_image(url=cont["url"])

                try:
                    embed.add_field(
                        name="**🖼 Download**",
                        value=f'**[➢ HD Download]({cont["hdurl"]})**',
                    )
                except KeyError:
                    pass

                embed.set_footer(
                    text=f"APOD Requested by {ctx.author.name}",
                    icon_url=ctx.author.avatar_url,
                )

                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Space(bot))
