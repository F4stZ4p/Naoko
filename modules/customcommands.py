import discord
import asyncpg
import random
import asyncio
from discord.ext import commands
from utils.naoko_paginator import NaokoPaginator

class CustomCommands():
    """Custom commands for your Discord server""" 
    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/nbEA3VE.png"
        self.commands = {}

    @property
    def length(self):
        """Returns total length of Custom Commands"""
        return len(self.commands)

    async def _load_customcommands(self):
        async with self.bot.db.acquire() as con:
            commands = await con.fetch("SELECT * FROM customcommands")
            for row in commands:
                self.commands.setdefault(row[0], {'': ''}).update(**{row[1]:row[2]})
        await self.bot.db.release(con)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def customcommand(self, ctx):
        """Manage custom commands"""
        await ctx.send(':information_source: | **Options available: ``add``, ``remove``, ``list``, ``removeall``**')

    @customcommand.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, commandname: str, *, commandtext: str):
        """Add custom command"""
        async with self.bot.db.acquire() as con:
            if (await con.fetchval('SELECT * FROM customcommands WHERE guildid = $1 AND name = $2', ctx.guild.id, commandname)) is None:
                try:
                    await con.execute('INSERT INTO customcommands ("guildid", "name", "action") VALUES ($1, $2, $3)', ctx.guild.id, commandname, commandtext)
                except Exception as e:
                    await ctx.send(f':warning: | **Your custom command is too long or error has occured: `{e}`**', delete_after=5)
            else:
                try:
                    await con.execute('UPDATE customcommands SET action = $1 WHERE guildid = $2 AND name = $3', commandtext, ctx.guild.id, commandname)
                except Exception as e:
                    await ctx.send(f':warning: | **Your custom command is too long or error has occured: `{e}`**', delete_after=5)
            try:
                self.commands[ctx.guild.id][commandname] = commandtext
            except KeyError:
                self.commands[ctx.guild.id] = {commandname: commandtext}
            await ctx.send(f':information_source: | **Custom command `{commandname}` successfully added**', delete_after=5)
        await self.bot.db.release(con)

    @customcommand.command(aliases=['delete'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx, *, commandname):
        """Remove custom command"""
        async with self.bot.db.acquire() as con:
            try:
                await con.execute('DELETE FROM customcommands WHERE guildid = $1 AND name = $2', ctx.guild.id, commandname)
                del self.commands[ctx.guild.id][commandname]
                await ctx.send(f':information_source: | **Custom command `{commandname}` was successfully removed**', delete_after=5)
            except:
                await ctx.send(f':warning: | **Custom command `{commandname}` does not exist**', delete_after=5)
        await self.bot.db.release(con)

    @customcommand.command(aliases=['discard', 'deleteall'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def removeall(self, ctx):
        """Remove all custom commands"""
        async with self.bot.db.acquire() as con:
            try:
                await con.execute('DELETE FROM customcommands WHERE guildid = $1', ctx.guild.id)
                await ctx.send(f':information_source: | **All custom commands were successfully removed**', delete_after=5)
            except:
                await ctx.send(f':warning: | **No custom commands in this server**', delete_after=5)
            try:
                del self.commands[ctx.guild.id]
            except:
                pass
        await self.bot.db.release(con)

    @customcommand.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def list(self, ctx):
        """Lists all custom commands"""
        try:
            await NaokoPaginator(entries=[c for c in self.commands[ctx.guild.id]], length=3, colour=random.randint(0x000000, 0xFFFFFF), title=f"{ctx.guild} Custom Commands").paginate(ctx)
        except:
            await ctx.send(f':warning: | **No custom commands in this server**', delete_after=5)

    async def on_ready(self):
        await asyncio.sleep(3)
        await self._load_customcommands()

    async def on_guild_remove(self, guild):
        async with self.bot.db.acquire() as con:
            try:
                await con.execute('DELETE FROM customcommands WHERE guildid = $1', guild.id)
                del self.commands[guild.id]
            except:
                pass
        await self.bot.db.release(con)


def setup(bot):
    bot.add_cog(CustomCommands(bot))