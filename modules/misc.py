import discord
import re
import random
import time
from discord.ext import commands
from datetime import datetime
from discord.ext.commands.cooldowns import BucketType


class Miscellaneous:
    """Miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot
        self._number_fmt = "\u20e3"
        self.thumbnail = "https://i.imgur.com/I3OYT4F.png"

    @commands.command()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def avatar(self, ctx, *, user: discord.User = None):
        if user is None:
            embed = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
            embed.set_image(url=ctx.author.avatar_url)
            embed.add_field(
                name="Here's avatar. Save it or drag to desktop",
                value=f"[Link]({ctx.author.avatar_url})",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
            embed.set_image(url=user.avatar_url)
            embed.add_field(
                name="Here's avatar. Save it or drag to desktop",
                value=f"[Link]({user.avatar_url})",
                inline=True,
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["patreon"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def donate(self, ctx):
        embed = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF), title="Support Naoko Bot"
        ).set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(
            name="**<:patreon:481802259764740097> Hello. Want to support the bot?**",
            value=f"```fix\nCurrently the bot is on {len(self.bot.guilds)} servers and it's growing! One small donation can help keep the bot running as long as it possible.```",
        )
        embed.add_field(
            name="**:thinking: Why should I donate?**",
            value="```fix\nIf you like the bot, you should donate to support its further development. Currently bot is selfhosted and I am looking for a good server.```",
        )
        embed.add_field(
            name="**:dark_sunglasses: So, how do I donate?**",
            value=f"Just go to **[Patreon](https://www.patreon.com/f4stz4p)** and donate 1$ or more. It can support the bot and you will get cool Donator role and cooldown-free commands use :) Once you've donated DM {self.bot.owner}",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def osu(self, ctx, osuplayer, hex: str = 170_041):
        embed = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
        embed.set_image(
            url="http://lemmmy.pw/osusig/sig.php?colour=hex{0}&uname={1}&pp=1&countryrank&removeavmargin&flagshadow&flagstroke&darktriangles&onlineindicator=undefined&xpbar&xpbarhex".format(
                hex, osuplayer
            )
        )
        embed.set_footer(
            text="Powered by lemmmy.pw",
            icon_url="https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/osusmall.ico",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1.0, 1000.0, commands.BucketType.user)
    async def report(self, ctx, *, trouble: str):
        """Reports a trouble to the developer team.
            @Naoko report Hi. I have a problem: something you want to report
        """
        try:
            await self.bot.get_channel(473_557_501_560_750_096).send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(name=f"**Report from {ctx.author}**", value=trouble)
                .set_footer(icon_url=ctx.author.avatar_url, text="Reported at: ")
            )
            await ctx.send(":ok_hand:", delete_after=5)
        except BaseException:
            await ctx.send(
                ":warning: | **Sorry, something went wrong while reporting.**"
            )

    @commands.command()
    @commands.cooldown(1.0, 1000.0, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion: str):
        """Suggests an idea to the developer team.
            @Naoko suggest Add more animal commands please!
        """
        try:
            await self.bot.get_channel(474_893_223_756_562_432).send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .add_field(name=f"**Suggestion from {ctx.author}**", value=suggestion)
                .set_footer(icon_url=ctx.author.avatar_url, text="Suggested at: ")
            )
            await ctx.send(":ok_hand:", delete_after=5)
        except BaseException:
            await ctx.send(
                ":warning: | **Sorry, something went wrong while suggesting.**"
            )

    @commands.command()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def ping(self, ctx):
        """Check bot reaction time!"""
        message = await ctx.send(
            embed=discord.Embed(
                title="Pinging...", color=random.randint(0x000000, 0xFFFFFF)
            ).set_footer(text="Wait a bit...", icon_url=ctx.author.avatar_url)
        )
        duration = message.created_at - ctx.message.created_at
        await message.edit(
            embed=discord.Embed(
                color=random.randint(0x000000, 0xFFFFFF),
                timestamp=ctx.message.created_at,
            )
            .add_field(
                name="**:ping_pong: Pong!**",
                value=f":heartbeat: **{round(self.bot.latency * 1000)}** ms\n:stopwatch: **{round(1000*duration.total_seconds())}** ms",
            )
            .set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        )

    @commands.command()
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def invite(self, ctx, botto: discord.User = None):
        """Invite me or any bot you want!"""
        botto = botto or ctx.me

        if not botto.bot:
            return await ctx.send(
                ":bangbang: | **This user is not a bot. You can't invite them!**",
                delete_after=5,
            )

        await ctx.send(
            embed=discord.Embed(
                color=random.randint(0x000000, 0xFFFFFF),
                timestamp=ctx.message.created_at,
            )
            .add_field(
                name=f"**:rose: Hey! Do you want to invite {botto.name}?**",
                value=f":sparkling_heart: If you want everything... **[● Invite](https://discordapp.com/oauth2/authorize?client_id={botto.id}&permissions=8&scope=bot)**\n:heartpulse: If you just want minimal permissions... **[● Invite](https://discordapp.com/oauth2/authorize?client_id={botto.id}&permissions=37080128&scope=bot)**",
            )
            .set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            .set_thumbnail(url=botto.avatar_url)
        )

    @commands.command()
    @commands.cooldown(1.0, 3.0, commands.BucketType.user)
    async def choose(self, ctx, *choices: commands.clean_content):
        """Wanna choose something? I can help you!"""
        await ctx.send(
            f":information_source: | {ctx.author.mention}, my choice is {random.choice(choices)}"
        )

    @commands.command()
    @commands.cooldown(1.0, 1.0, commands.BucketType.user)
    async def nitro(self, ctx, *, emoji: commands.clean_content):
        """Allows you to use nitro emoji
        ------
        n.nitro thonk
        Will send a thonk emoji in chat
        """
        try:
            await ctx.send(
                discord.utils.find(
                    lambda e: e.name.lower() == emoji.lower(), self.bot.emojis
                )
            )
        except BaseException:
            await ctx.send(
                f":warning: | **Sorry, no matches found for `{emoji.lower()}`**",
                delete_after=5,
            )

    @commands.command(aliases=["chain"])
    @commands.guild_only()
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def markov(self, ctx):
        """Generates a Markov Chain"""
        async with ctx.typing():
            try:
                await ctx.send(
                    embed=discord.Embed(
                        title="Markov Chain",
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                    )
                    .add_field(
                        name="**:link: Chain**",
                        value=" ".join(
                            random.sample(
                                [
                                    m.clean_content
                                    for m in await ctx.channel.history(
                                        limit=150
                                    ).flatten()
                                    if not m.author.bot
                                ],
                                10,
                            )
                        ),
                    )
                    .set_footer(
                        text=f"Markov Chain for #{ctx.channel.name}",
                        icon_url=ctx.guild.icon_url,
                    )
                    .add_field(
                        name="**:recycle: Messages Analyzed**",
                        value="Analyzed **150** messages",
                    )
                )
            except BaseException:
                await ctx.send(":warning: | **An error occured**", delete_after=5)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def poll(self, ctx, title: str, *variants):
        """
        Starts a poll
        For example, n.poll "Best Bot" Naoko MEE6 Rythm Dyno
        """
        if 1 >= len(variants) or len(variants) > 10:
            await ctx.send(
                "<:Error:501773759217401856> | **You can't start a poll with less than 1 variant or more than 10 variants**",
                delete_after=10,
            )
        else:
            try:
                await ctx.message.delete()
            except BaseException:
                pass

            m = await ctx.send(
                embed=discord.Embed(
                    timestamp=ctx.message.created_at,
                    title=title if len(title) < 30 else f"{title[:30]}...",
                    colour=random.randint(0x000000, 0xFFFFFF),
                    description="\n".join(
                        [
                            f'{index}{self._number_fmt}: **{value if len(value) < 150 else f"{value[:147]}..."}**'
                            for index, value in enumerate(variants)
                        ]
                    ),
                ).set_footer(
                    text=f"Poll by {ctx.author.name}", icon_url=ctx.author.avatar_url
                )
            )
            for index in range(len(variants)):
                await m.add_reaction(f"{index}{self._number_fmt}")


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
