import discord
from io import BytesIO
from discord.ext import commands

class Cloud():
    """Naoko Cloud. Upload anything you want except NSFW content"""
    def __init__(self, bot):
        self.bot = bot
        self.server = "http://62.210.7.8:6980"
        self.thumbnail = "https://i.imgur.com/umEfgUN.png"

    @commands.command()
    async def upload(self, ctx):
        temp_bytes = BytesIO()
        
        await ctx.message.attachments[0].save(temp_bytes)
        temp_bytes.seek(0)
        async with ctx.typing():
            async with self.bot.session.post(f"{self.server}/up", data={"file": temp_bytes}) as r:
                await ctx.send((await r.text()))

def setup(bot):
    bot.add_cog(Cloud(bot))