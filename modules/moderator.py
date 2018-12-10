import asyncio
import random
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType


class Moderator:
    """Ultracool moderator commands"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/ThgHDAA.png"

    @commands.command(name="kick", aliases=["k"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, target: discord.User, *, reason: str = None):
        """Kicks an annoying user. Requires kick members permission. Also bot must have this permission."""
        if reason is None:
            reason = "No reason specified"
        embedkick = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF),
            timestamp=ctx.message.created_at,
            title=f"Kick | {ctx.author.name} 👢 {target.name}",
        )
        embedkick.set_thumbnail(url=target.avatar_url)
        embedkick.add_field(
            name=f"**🔴 Kick Info**",
            value=f":spy: Responsible Moderator: **{ctx.author.mention}**\n:book: Reason: **{reason if len(reason) <= 100 else f'{reason[:100]}...'}**\n:stopwatch: Time: **{ctx.message.created_at}**",
        )
        embedkick.set_footer(text=ctx.guild, icon_url=ctx.guild.icon_url)
        try:
            await ctx.guild.kick(
                target,
                reason=f"{ctx.author}: {reason if len(reason) <= 100 else f'{reason[:100]}...'}",
            )
            await ctx.send(embed=embedkick)
        except:
            await ctx.send(
                "**:x: Sorry, I am missing permissions to do this!**", delete_after=10
            )

    @commands.command(name="ban", aliases=["b"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, target: discord.User, *, reason: str = None):
        """Bans an annoying user. Requires ban members permission. Also bot must have this permission."""
        if reason is None:
            reason = "No reason specified"
        embedban = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF),
            timestamp=ctx.message.created_at,
            title=f"Ban | {ctx.author.name} 🔨 {target.name}",
        )
        embedban.set_thumbnail(url=target.avatar_url)
        embedban.add_field(
            name=f"**🔴 Ban Info**",
            value=f":spy: Responsible Moderator: **{ctx.author.mention}**\n:book: Reason: **{reason if len(reason) <= 100 else f'{reason[:100]}...'}**\n:stopwatch: Time: **{ctx.message.created_at}**",
        )
        embedban.set_footer(text=ctx.guild, icon_url=ctx.guild.icon_url)
        try:
            await ctx.guild.ban(
                target,
                reason=f"{ctx.author}: {reason if len(reason) <= 100 else f'{reason[:100]}...'}",
            )
            await ctx.send(embed=embedban)
        except:
            await ctx.send(
                "**:x: Sorry, I am missing permissions to do this!**", delete_after=10
            )

    @commands.command(name="unban", aliases=["ub"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, target: discord.User, *, reason: str = None):
        """Unbans an user. Requires ban members permission. Also bot must have this permission."""
        if reason is None:
            reason = "No reason specified"
        embedunban = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF),
            timestamp=ctx.message.created_at,
            title=f"Unban | {ctx.author.name} ❌🔨 {target.name}",
        )
        embedunban.set_thumbnail(url=target.avatar_url)
        embedunban.add_field(
            name=f"**🔴 Unban Info**",
            value=f":spy: Responsible Moderator: **{ctx.author.mention}**\n:book: Reason: **{reason if len(reason) <= 100 else f'{reason[:100]}...'}**\n:stopwatch: Time: **{ctx.message.created_at}**",
        )
        embedunban.set_footer(text=ctx.guild, icon_url=ctx.guild.icon_url)
        try:
            await ctx.guild.unban(
                target,
                reason=f"{ctx.author}: {reason if len(reason) <= 100 else f'{reason[:100]}...'}",
            )
            await ctx.send(embed=embedunban)
        except:
            await ctx.send(
                "**:x: Sorry, I am missing permissions to do this!**", delete_after=10
            )

    @commands.command(name="purge", aliases=["pg", "massclean", "massdelete"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def _purge(self, ctx, count: int):
        """Purges messages. Requires manage messages permission"""
        if count > 1000 or count < 1:
            await ctx.send(
                ":warning: | **Count can't be lesser than 0 and greater than 1000**",
                delete_after=10,
            )

        else:
            try:
                await ctx.channel.purge(limit=count)
                await ctx.send(
                    f"**I have deleted ``{count}`` messages for you! <a:rem:466165862710247424>**",
                    delete_after=10,
                )
            except:
                await ctx.send(
                    "**:x: Sorry, I am missing permissions to do this or messages are too old**",
                    delete_after=10,
                )

    @commands.command(name="mute")
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def _mute(self, ctx, user: discord.Member, *, reason: str):
        """Mutes an annoying user. Requires Manage Roles permission"""
        try:
            await ctx.channel.set_permissions(
                user, send_messages=False, reason=f"{ctx.author}: {reason}"
            )
        except:
            await ctx.send(":thumbsdown:")
        else:
            await ctx.send(":ok_hand:")

    @commands.command(name="unmute")
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def _unmute(self, ctx, user: discord.Member, *, reason: str):
        """Unmutes an user. Requires Manage Roles permission"""
        try:
            await ctx.channel.set_permissions(
                user, send_messages=True, reason=f"{ctx.author}: {reason}"
            )
        except:
            await ctx.send(":thumbsdown:")
        else:
            await ctx.send(":ok_hand:")


def setup(bot):
    bot.add_cog(Moderator(bot))
