import discord
from io import BytesIO
from discord.ext import commands

class Cloud():
    """Naoko Cloud. Upload anything you want except NSFW content"""
    def __init__(self, bot):
        self.bot = bot
        self.server = "62.210.7.8:6980"
        self.thumbnail = "https://i.imgur.com/umEfgUN.png"

    @commands.command()
    async def upload(self, ctx):
        file = (await ctx.message.attachments[0].save(fp=BytesIO())).read()
        async with ctx.typing():
            async with self.bot.session.post(f"{self.server}/up", data={"file": file}) as r:
                await ctx.send((await r.text()))

def setup(bot):
    bot.add_cog(Cloud(bot))