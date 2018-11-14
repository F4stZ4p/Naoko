import discord
import asyncpg
import asyncio
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Settings:
    """Set me up the way you want to~"""
    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/IYPhR30.png"

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1.0, 10.0, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx):
        """Set up bot the way you want"""
        await ctx.send(':information_source: | **Available options: ``prefix`` ; ``resetprefix``**', delete_after=15)

    @settings.command()
    @commands.guild_only()
    @commands.cooldown(1.0, 10.0, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        """Set custom guild prefix. Requires Manage Server permission."""
        if len(prefix) > 50 or len(prefix) < 1:
            await ctx.send(":warning: | **Prefix can't be longer than 50 characters or shorter than 1 character**", delete_after=15)
        else:
            async with self.bot.db.acquire() as con:
                a = await con.fetchval(f'SELECT * FROM prefix WHERE GUILDID = {ctx.guild.id};')
                if a is not None:
                    await con.execute('UPDATE prefix SET prefix=$1 WHERE "guildid"=$2;', prefix, ctx.guild.id)
                    await ctx.send(f':white_check_mark: | **Updated guild prefix to ``{prefix}``**'.replace('@', '@\u200b'), delete_after=15)
                else:
                    await con.execute('INSERT INTO prefix (GUILDID, PREFIX) VALUES ($1, $2)', ctx.guild.id, prefix)
                    await ctx.send(f':white_check_mark: | **Set guild prefix to ``{prefix}``**'.replace('@', '@\u200b'), delete_after=15)
            self.bot.all_prefixes[ctx.guild.id] = prefix
            await self.bot.db.release(con)

    @settings.command()
    @commands.guild_only()
    @commands.cooldown(1.0, 10.0, commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def resetprefix(self, ctx):
        """Reset guild prefix"""
        async with self.bot.db.acquire() as con:
            try:
                await con.execute('DELETE FROM prefix WHERE GUILDID=$1;', ctx.guild.id)
                del self.bot.all_prefixes[ctx.guild.id]
                await ctx.send(f':white_check_mark: | **Reset default guild prefix**', delete_after=15)
            except:
                await ctx.send(':question: | **No custom guild prefix was specified**', delete_after=15)
        await self.bot.db.release(con)

def setup(bot):
    bot.add_cog(Settings(bot))