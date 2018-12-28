import traceback
import sys
from discord.ext import commands
from datetime import timedelta
import discord
import random
import checks.naoko_checks


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot
        bot.on_command_error = self._on_command_error

    async def _on_command_error(self, ctx, error, bypass=False):
        if (hasattr(ctx.command, "on_error") or (ctx.command and hasattr(
                ctx.cog, f"_{ctx.command.cog_name}__error")) and not bypass):
            return

        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like you're missing a required argument:**",
                    value=f":warning: Error: `{error}`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like you gave me a bad argument:**",
                    value=f":warning: Error: `{error}`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )

        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id not in self.bot.patrons:
                return await ctx.send(
                    embed=discord.Embed(
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                    )
                    .add_field(
                        name=f"**Seems like you are on cooldown:**",
                        value=f":clock11: Remaining time: `{timedelta(seconds=int(error.retry_after))}`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`\n<:patreon:481802259764740097> Alternative: `be a Patron and have no cooldowns`".replace(
                            ctx.me.mention, f"@{self.bot.user.name}"
                        ),
                    )
                    .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                    delete_after=10,
                )
        elif isinstance(error, discord.Forbidden):
            pass
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like you can't use this command in private messages:**",
                    value=f":question: What to do: `invite me to a server using link in {ctx.prefix}about!`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )

        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, checks.naoko_checks.OwnerOnly):
                pass
            elif isinstance(error, checks.naoko_checks.NSFWOnly):
                await ctx.send(
                    embed=discord.Embed(
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                    )
                    .add_field(
                        name=f"**Seems like you can't use this command here:**",
                        value=f":warning: Error: `this command can be used only in NSFW channels.`",
                    )
                    .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                    delete_after=10,
                )
            elif isinstance(error, checks.naoko_checks.PatronOnly):
                await ctx.send(
                    embed=discord.Embed(
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                    )
                    .add_field(
                        name=f"**Seems like you can't use this command:**",
                        value=f":warning: Error: `this command is only for Patreon supporters`\n<:patreon:481802259764740097> Alternative: `be a Patron and unlock this command`",
                    )
                    .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                    delete_after=10,
                )
            elif isinstance(error, checks.naoko_checks.NeedsAccount):
                await ctx.send(
                    embed=discord.Embed(
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                    )
                    .add_field(
                        name=f"**Seems like you can't use this command:**",
                        value=f":warning: Error: `you need an Economy Account`\n:information_source: Solution: `do {ctx.prefix}create to create one!`",
                    )
                    .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                    delete_after=10,
                )
            else:
                await ctx.send(
                    embed=discord.Embed(
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                    )
                    .add_field(
                        name=f"**Seems like you can't use this command:**",
                        value=f":warning: Error: `{error}`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                            ctx.me.mention, f"@{self.bot.user.name}"
                        ),
                    )
                    .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                    delete_after=10,
                )

        elif isinstance(error, discord.HTTPException):
            pass

        elif isinstance(error, commands.UserInputError):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like you did something wrong:**",
                    value=f":question: What to do: `look at {ctx.prefix}help and try being more specific`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like you are missing permissions:**",
                    value=f":warning: Error: `{error}`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )

        elif isinstance(error, commands.DisabledCommand):
            return

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like something went wrong while executing command:**",
                    value=f":question: What to do: `join support server and report this issue to developer. Link can be found in {ctx.prefix}about`\n:warning: Error: `{error}`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like you gave me too many arguments:**",
                    value=f":question: What to do: `look at {ctx.prefix}help and try being more specific`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(
                    name=f"**Seems like I am missing permissions:**",
                    value=f":warning: Error: `{error}`\n:information_source: Command usage: `{ctx.prefix}{ctx.command.signature}`".replace(
                        ctx.me.mention, f"@{self.bot.user.name}"
                    ),
                )
                .set_footer(text=ctx.author, icon_url=ctx.author.avatar_url),
                delete_after=10,
            )


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
