import discord
from discord.ext import commands
from collections import deque

class SnipeHistory(deque):
    def __init__(self):
        super().__init__(maxlen=5)

    def __repr__(self):
        return "Naoko Snipe History"

class Snipes():
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}
        self.thumbnail = self.bot.user.avatar_url
        
    async def on_message_delete(self, message):
        if message.channel.is_nsfw():
            return
        
        try:
            self.snipes[message.channel.id].appendleft(message)
        except:
            self.snipes[message.channel.id] = SnipeHistory()
            self.snipes[message.channel.id].appendleft(message)
        
    @commands.command()
 #   @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def snipe(self, ctx, channel: discord.TextChannel = None, index: int = 0):
        channel = channel or ctx.channel
        
        if channel.is_nsfw():
            await ctx.send('Attempting to snipe a NSFW channel')
        
        else:
            sniped = self.snipes[channel.id][index]
            
            await ctx.send(f'Message sniped by {sniped.author}\n\n{sniped.clean_content}')
            
def setup(bot):
    bot.add_cog(Snipes(bot))
