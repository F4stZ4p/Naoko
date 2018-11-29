import discord
from discord.ext import commands
from collections import deque

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
        
        self.bot.loop.create_task(self.cleanup())
        
    async def cleanup(self):
        """Background loop to clean up snipe cache"""
        
        await asyncio.sleep(600) # snipes will be stored for 10 minutes
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
    async def snipe(self, ctx, channel: discord.TextChannel = None, index: int = None):
        
        channel = channel or ctx.channel
        index = index-1 or 0
        
        if channel.is_nsfw():
            await ctx.send('Attempting to snipe a NSFW channel')
        
        else:
            sniped = self.snipes[channel.id][index]
            
            await ctx.send(embed=discord.Embed(color=ctx.author.top_role.colour, title=f"@{sniped.author} said in #{sniped.channel}", description=sniped.clean_content))
            
    @snipe.error
    async def snipe_error(self, error, ctx):
        await ctx.send(':warning: | **No things to snipe in this channel or your index is invalid and must be in range 1-5**', delete_after=10)       
            
def setup(bot):
    bot.add_cog(Snipes(bot))
