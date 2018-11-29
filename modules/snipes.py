import discord
from discord.ext import commands

from collections import deque
from random import randint as r

class SnipeHistory(deque):
    def __init__(self):
        super().__init__(maxlen=5)

    def __repr__(self):
        return "Naoko Snipe History"

class Snipes():
    """Snipe anything deleted"""
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}
        self.thumbnail = self.bot.user.avatar_url
        
    def cleanup(self):
        """Function to clean up snipe cache"""
        self.snipes = {}
    
    async def on_message_delete(self, message):
        """Event is triggered when message is deleted"""
        if message.channel.is_nsfw():
            return
        
        try:
            self.snipes[message.channel.id].appendleft(message)
        except:
            self.snipes[message.channel.id] = SnipeHistory().appendleft(message)
        
    @commands.command()
 #   @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def snipe(self, ctx, channel: discord.TextChannel = None, index: int = 0):
        
        channel = channel or ctx.channel

        if index != 0:
            index = index-1

        if channel.is_nsfw():
            await ctx.send('Attempting to snipe a NSFW channel')

        else:
            sniped = self.snipes[channel.id][index]
            
            await ctx.send(embed=discord.Embed(color=r(0x000000, 0xFFFFFF), 
                                               timestamp=sniped.created_at,
                                               title=f"@{sniped.author} said in #{sniped.channel}", 
                                               description=sniped.clean_content).set_thumbnail(url=sniped.author.avatar_url).set_footer(text=f"Sniped by {ctx.author.name} | Message created", icon_url=ctx.author.avatar_url))
   
    @snipe.error
    async def snipe_error(self, error, ctx):
        await ctx.send(':warning: | **Invalid channel or index is greater than 5 or lesser than 1**', delete_after=10)

def setup(bot):
    bot.add_cog(Snipes(bot))
