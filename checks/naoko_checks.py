import discord
from discord.ext import commands

class NSFWOnly(commands.CheckFailure):
    pass

class OwnerOnly(commands.CheckFailure):
    pass

class PatronOnly(commands.CheckFailure):
    pass

class NeedsAccount(commands.CheckFailure):
    pass

def nsfw():
    async def predicate(ctx):
        if type(ctx.channel) == discord.channel.DMChannel:
            raise NSFWOnly()
        elif ctx.channel.is_nsfw():
            return True
        else:
            raise NSFWOnly()
    return commands.check(predicate)

def owner():
    async def predicate(ctx):
        if ctx.author.id in ctx.bot.whitelist:
            return True
        else:
            raise OwnerOnly()
    return commands.check(predicate)

def patron():
    async def predicate(ctx):
        if ctx.author.id in ctx.bot.patrons:
            return True
        else:
            raise PatronOnly()
    return commands.check(predicate)

def account():
    async def predicate(ctx):
        if (await ctx.bot.db.fetchval(f'SELECT * FROM users WHERE id = {ctx.author.id}')) is not None:
            return True
        else:
            raise NeedsAccount()
    return commands.check(predicate)