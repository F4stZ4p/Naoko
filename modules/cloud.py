import discord
from discord.ext import commands

class Cloud():
    """Naoko Cloud. Upload anything you want except NSFW content"""
    def __init__(self, bot):
        self.bot = bot
        self.uploads_destination = self.bot.get_channel(513440818439389214)
        self.thumbnail = "https://i.imgur.com/umEfgUN.png"

    @commands.command()
    async def upload(self, ctx):
        b = await self.uploads_destination.send(content=f"Upload by: **{ctx.author}** | ID: **{ctx.author.id}**", file=discord.File(ctx.message.attachments[0]))
        await ctx.send(b.attachments[0].url)

def setup(bot):
    bot.add_cog(Cloud(bot))