import discord
from discord.ext import commands
import random
import aiohttp
import math
import asyncio
from discord.ext.commands.cooldowns import BucketType
from urllib.parse import quote
import re
import uuid
import html
from utils.naoko_paginator import NaokoPaginator


class Fun:
    """Let's have some fun!"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/SIvBakG.png"
        self.emoji_true = "🔵"
        self.emoji_false = "🔴"
        self.user = self.bot.config.cleverbot_user
        self.cleverbotapikey = self.bot.config.cleverbot_key
        self.ytapikey = self.bot.config.youtube_key
        self.lyricskey = self.bot.config.lyrics_key
        self.session = self.bot.session

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def color(self, ctx, user: discord.Member = None):
        """ Gives your or target's highest role colour """
        if user is None:
            embed = discord.Embed(color=ctx.author.top_role.colour)
            embed.set_footer(
                text=f"{ctx.author}'s highest role color is: {ctx.author.top_role.colour}"
            )
            await ctx.send(embed=embed)
        else:
            try:
                embed = discord.Embed(color=user.top_role.colour)
                embed.set_footer(
                    text=f"{user}'s highest role color is: {user.top_role.colour}"
                )
                await ctx.send(embed=embed)
            except Exception:
                pass

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def rip(self, ctx, *, text: str):
        """ RIPs a user """
        rip = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
        rip.set_image(
            url=f"http://www.tombstonebuilder.com/generate.php?top1={quote(text)}&top2=&top3=&top4=&sp="
        )
        await ctx.send(embed=rip)

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def randomlove(self, ctx):
        """ Calculates random users love percentage """
        love = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF),
            title="Random Users Love Calculator!",
        )
        love.set_footer(
            text=f"{random.choice(ctx.guild.members)} loves {random.choice(ctx.guild.members)} for {random.randint(0, 100)}%",
            icon_url="https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/heart.png",
        )
        await ctx.send(embed=love)

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def profile(self, ctx, userfoo: discord.Member = None):
        """ Generates your profile card """
        if userfoo == None:
            profembed = discord.Embed(
                color=ctx.author.top_role.colour, title=f"{ctx.author}'s profile card"
            )
            profembed.add_field(
                name=":comet: ``Status:``",
                value=f"``{ctx.author.status}``",
                inline=True,
            )
            profembed.add_field(
                name=":video_game: ``Playing:``",
                value=f"``{ctx.author.activity}``",
                inline=True,
            )
            profembed.add_field(
                name=":robot: ``Is bot:``", value=f"``{ctx.author.bot}``", inline=True
            )
            profembed.add_field(
                name=":tophat: ``Created at:``",
                value=f"``{ctx.author.created_at}``",
                inline=True,
            )
            profembed.add_field(
                name=":crown: ``Top role:``",
                value=f"``{ctx.author.top_role}``",
                inline=True,
            )
            profembed.add_field(
                name=":frame_photo: ``Avatar URL:``",
                value=f"**[URL]({ctx.author.avatar_url})**",
                inline=True,
            )
            profembed.add_field(
                name=":art: ``Highest role colour:``",
                value=f"``{ctx.author.top_role.colour}``",
                inline=True,
            )
            profembed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=profembed)
        else:
            profembed = discord.Embed(
                color=userfoo.top_role.colour, title=f"{userfoo}'s profile card"
            )
            profembed.add_field(
                name=":comet: ``Status:``", value=f"``{userfoo.status}``", inline=True
            )
            profembed.add_field(
                name=":video_game: ``Playing:``",
                value=f"``{userfoo.activity}``",
                inline=True,
            )
            profembed.add_field(
                name=":robot: ``Is bot:``", value=f"``{userfoo.bot}``", inline=True
            )
            profembed.add_field(
                name=":tophat: ``Created at:``",
                value=f"``{userfoo.created_at}``",
                inline=True,
            )
            profembed.add_field(
                name=":crown: ``Top role:``",
                value=f"``{userfoo.top_role}``",
                inline=True,
            )
            profembed.add_field(
                name=":frame_photo: ``Avatar URL:``",
                value=f"**[URL]({userfoo.avatar_url})**",
                inline=True,
            )
            profembed.add_field(
                name=":art: ``Highest role colour:``",
                value=f"``{userfoo.top_role.colour}``",
                inline=True,
            )
            profembed.set_thumbnail(url=userfoo.avatar_url)
            await ctx.send(embed=profembed)

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def reverse(self, ctx, *, texttoreverse):
        """ Gives you reversed text """
        encodes = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
        encodes.add_field(name="Reversed:", value=f"```{texttoreverse[::-1]}```")
        encodes.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=encodes)

    @commands.command(pass_context=True, aliases=["hb"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def hastebin(self, ctx, *, stringx):
        """ Uploads text to Hastebin """
        hastem = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
        async with self.session.post(
            "https://hastebin.com/documents", data=stringx.encode("utf-8")
        ) as post:
            post = await post.json()
        hastem.add_field(
            name="Uploaded!",
            value="**[URL to Hastebin](https://hastebin.com/{})**".format(post["key"]),
        )
        hastem.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=hastem)

    @commands.command(pass_context=True, aliases=["mb"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def mystbin(self, ctx, *, stringx):
        """ Uploads text to Mystbin """
        mystem = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
        async with self.session.post(
            "http://mystb.in/documents", data=stringx.encode("utf-8")
        ) as post:
            post = await post.json()
        mystem.add_field(
            name="Uploaded!",
            value="**[URL to Mystbin](http://mystb.in/{})**".format(post["key"]),
        )
        mystem.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=mystem)

    @commands.command(pass_context=True, aliases=["cat"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def randomcat(self, ctx):
        """ Gives you random photo of a cat """
        try:
            async with self.session.get("http://aws.random.cat/meow") as resp:
                data = await resp.json()
                embedssss = discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    title="Random Cat Image :3",
                )
                embedssss.set_image(url=data["file"])
                embedssss.set_footer(
                    text=f"Requested by: {ctx.author}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                await ctx.send(embed=embedssss)
        except Exception:
            emdexs = discord.Embed(color=0x170041)
            emdexs.set_footer(
                text="API is unavailable now. Try again later!",
                icon_url="https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/error.ico",
            )
            await ctx.send(embed=emdexs)

    @commands.command(pass_context=True, aliases=["dog"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def randomdog(self, ctx):
        """ Gives you random photo of a dog """
        try:
            async with self.session.get("https://random.dog/woof.json") as resp:
                data = await resp.json()
                sender = data["url"]
                embedssss = discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    title="Random Dog Image :3",
                )
                embedssss.set_image(url=sender)
                embedssss.set_footer(
                    text=f"Requested by: {ctx.author}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                await ctx.send(embed=embedssss)
        except Exception:
            emdexs = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
            emdexs.set_footer(
                text="API is unavailable now. Try again later!",
                icon_url="https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/error.ico",
            )
            await ctx.send(embed=emdexs)

    @commands.command(pass_context=True, aliases=["w"])
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def weather(self, ctx, *, location):
        """
        Gives you weather in requested city or region.
        For example, @Naoko weather London will give you current weather in London.
        """
        try:
            async with self.session.get(
                f"http://openweathermap.org/data/2.5/weather?q={location}&appid=b6907d289e10d714a6e88b30761fae22"
            ) as resp:
                data = await resp.json()
                if data["cod"] == 200:
                    await NaokoPaginator(
                        colour=random.randint(0x000000, 0xFFFFFF),
                        title=f'Weather: {data["sys"].get("country")} | {data["name"]}',
                        entries=[
                            f':sunny: **Main**\n```Current state - {data["weather"][0].get("main")}: {data["weather"][0].get("description")}\nTemperature: {data["main"].get("temp")}°C\nPressure: {data["main"].get("pressure")} hPa\nHumidity: {data["main"].get("humidity")}%\nMin. temperature: {data["main"].get("temp_min")}°C\nMax. temperature: {data["main"].get("temp_max")}°C\nVisibility: {data.get("visibility")} metres```',
                            f':dart: **Coordinates**\n```Latitude: {data["coord"].get("lat")} | Longitude: {data["coord"].get("lon")}```',
                            f':cloud: **Clouds**\n```{data["clouds"].get("all")}%```',
                        ],
                        length=1,
                    ).paginate(ctx)

        except:
            emdexsssssss = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
            emdexsssssss.set_footer(
                text=f"API error or no weather results found for {location}.",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=emdexsssssss)

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def dice(self, ctx):
        """Throws a random dice"""
        embed = discord.Embed(color=1_507_393)
        embed.set_image(
            url="https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/{}.png".format(
                random.randint(1, 6)
            )
        )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["btc"])
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def bitcoin(self, ctx, currency: str = None):
        """
        Gives you bitcoin cost.
        For example, @Naoko bitcoin USD will give you currency in US $
        """
        if currency is None:
            embederror = discord.Embed(color=0xFF9900)
            embederror.set_footer(
                text="You forgot the currency.",
                icon_url="http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/bitcoin-icon.png",
            )
            await ctx.send(embed=embederror)

        else:
            try:
                async with self.session.get("https://blockchain.info/ticker") as resp:
                    data = await resp.json()
                    embedbtc = discord.Embed(
                        title=f"Bitcoin Price - in {data[currency.upper()].get('symbol')}",
                        color=0xFF9900,
                    )
                    embedbtc.set_thumbnail(
                        url="http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/bitcoin-icon.png"
                    )
                    embedbtc.add_field(
                        name="Last 15 minutes",
                        value=f"**{round(data[currency.upper()].get('15m'))} {data[currency.upper()].get('symbol')}**",
                        inline=True,
                    )
                    embedbtc.add_field(
                        name="Last",
                        value=f"**{round(data[currency.upper()].get('last'))} {data[currency.upper()].get('symbol')}**",
                        inline=True,
                    )
                    embedbtc.add_field(
                        name="Buy",
                        value=f"**{round(data[currency.upper()].get('buy'))} {data[currency.upper()].get('symbol')}**",
                        inline=True,
                    )
                    embedbtc.add_field(
                        name="Sell",
                        value=f"**{round(data[currency.upper()].get('sell'))} {data[currency.upper()].get('symbol')}**",
                        inline=True,
                    )
                    embedbtc.set_footer(
                        text=f"Command requested by {ctx.author}",
                        icon_url=ctx.author.avatar_url,
                    )
                    await ctx.send(embed=embedbtc)

            except:
                emdexs = discord.Embed(color=0xFF9900)
                emdexs.set_footer(
                    text=f"No results found for currency - {currency}",
                    icon_url="http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/bitcoin-icon.png",
                )
                await ctx.send(embed=emdexs)

    @commands.command(pass_context=True, aliases=["ryt"])
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def randomyt(self, ctx):
        """Generates random YouTube video"""
        try:
            async with self.session.get(
                f"https://randomyoutube.net/api/getvid?api_token={self.ytapikey}"
            ) as resp:
                data = await resp.json()
                embedyt = discord.Embed(color=0xFF0000)
                embedyt.add_field(
                    name="**Here's your random YouTube video!**",
                    value=f"**[Link](https://youtube.com/watch/{data['vid']})**",
                )
                embedyt.set_image(
                    url=f"https://img.youtube.com/vi/{data['vid']}/hqdefault.jpg"
                )
                await ctx.send(embed=embedyt)
        except:
            emdexs = discord.Embed(color=0x170041)
            emdexs.set_footer(
                text="API is unavailable now. Try again later!",
                icon_url="https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/error.ico",
            )
            await ctx.send(embed=emdexs)

    @commands.command(pass_context=True)
    @commands.cooldown(3.0, 10.0, commands.BucketType.guild)
    async def ask(self, ctx, *, textfield):
        async with ctx.typing():
            async with self.session.post(
                "https://cleverbot.io/1.0/ask",
                data={
                    "user": self.user,
                    "key": self.cleverbotapikey,
                    "nick": "Naoko",
                    "text": textfield,
                },
            ) as resp:
                data = await resp.json()
                await ctx.send(f'{ctx.author.mention}, {data.get("response")}')

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def bigmoji(self, ctx, *, emoji):
        """ Reveals an emoji """
        emoji = re.findall("(\d+)", emoji)[0]
        embedemo = discord.Embed(color=0x36393E, title=f"Emoji: {emoji}")
        embedemo.add_field(
            name="**Download link**",
            value=f"**[➤ URL](https://cdn.discordapp.com/emojis/{emoji})**",
        )
        embedemo.set_image(url=f"https://cdn.discordapp.com/emojis/{emoji}")
        embedemo.set_footer(
            text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url
        )
        embedemo.timestamp = ctx.message.created_at
        await ctx.send(embed=embedemo)

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def uuid(self, ctx):
        """ Generates a random UUID """
        embeduuid = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF),
            description=f"```ini\n[{uuid.uuid4()}]```",
            timestamp=ctx.message.created_at,
        )
        embeduuid.set_footer(
            text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embeduuid)

    @commands.command(pass_context=True)
    @commands.cooldown(1.0, 25.0, commands.BucketType.channel)
    async def trivia(self, ctx):
        def reactcheck(reaction, user):
            return user != ctx.me and str(reaction.emoji) in [
                self.emoji_true,
                self.emoji_false,
            ]

        async with self.session.get(
            "https://opentdb.com/api.php?amount=1&type=boolean"
        ) as resp:
            data = await resp.json()
            if data["response_code"] == 0:
                if data["results"][0].get("difficulty") == "easy":
                    color = int(0x32CD32)
                if data["results"][0].get("difficulty") == "medium":
                    color = int(0xFF4500)
                if data["results"][0].get("difficulty") == "hard":
                    color = int(0xFF0000)
                embedtrivia = discord.Embed(color=color)
                embedtrivia.set_author(
                    name=f'Question: {html.unescape(data["results"][0].get("question"))}',
                    icon_url=ctx.guild.icon_url,
                )
                embedtrivia.add_field(
                    name=f"**Category:**",
                    value=f'```{data["results"][0].get("category")}```',
                    inline=False,
                )
                embedtrivia.add_field(
                    name=f"**Difficulty:**",
                    value=f'```{data["results"][0].get("difficulty").upper()}```',
                    inline=False,
                )
                embedtrivia.add_field(
                    name="**Answers:**",
                    value=f"```{self.emoji_true} - True | {self.emoji_false} - False```",
                    inline=False,
                )
                msg = await ctx.send(embed=embedtrivia, delete_after=25)
                await msg.add_reaction(self.emoji_true)
                await msg.add_reaction(self.emoji_false)

                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add", timeout=15.0, check=reactcheck
                    )
                except asyncio.TimeoutError:
                    embednew = discord.Embed(color=color)
                    embednew.set_author(
                        name=f'Question was: {html.unescape(data["results"][0].get("question"))}',
                        icon_url=ctx.guild.icon_url,
                    )
                    embednew.set_footer(
                        text=f'Trivia timed out. The correct answer was {data["results"][0].get("correct_answer")}!'
                    )
                    await msg.edit(embed=embednew, delete_after=5)

                else:
                    if str(reaction.emoji) == self.emoji_true:
                        if data["results"][0].get("correct_answer") == "True":
                            response = "correct!"
                        embednew = discord.Embed(color=color)
                        embednew.set_author(
                            name=f'Question was: {html.unescape(data["results"][0].get("question"))}',
                            icon_url=ctx.guild.icon_url,
                        )
                        embednew.set_footer(
                            text=f"{user} answered True. It was {response}",
                            icon_url=user.avatar_url,
                        )
                        await msg.edit(embed=embednew, delete_after=5)

                    elif str(reaction.emoji) == self.emoji_false:
                        if data["results"][0].get("correct_answer") == "True":
                            responsetwo = "incorrect!"
                        embednew = discord.Embed(color=color)
                        embednew.set_author(
                            name=f'Question was: {html.unescape(data["results"][0].get("question"))}',
                            icon_url=ctx.guild.icon_url,
                        )
                        embednew.set_footer(
                            text=f"{user} answered False. It was {responsetwo}",
                            icon_url=user.avatar_url,
                        )
                        await msg.edit(embed=embednew, delete_after=5)

    @commands.command(name="randomfox", aliases=["fox"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def _randomfox(self, ctx):
        """Gives you random image of a fox"""
        async with self.session.get("https://randomfox.ca/floof/") as resp:
            data = await resp.json()
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                    title="Fox image :3",
                )
                .set_image(url=data["image"])
                .set_footer(
                    text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url
                )
            )

    @commands.command()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def catfact(self, ctx):
        """Gives you random cat fact"""
        try:
            async with self.session.get("https://catfact.ninja/fact") as resp:
                data = await resp.json()
                await ctx.send(
                    embed=discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
                    .add_field(
                        name="**:cat: Random cat fact**",
                        value=f"```fix\n{data.get('fact')}```",
                    )
                    .set_footer(
                        text=f"Cat fact requested by: {ctx.author}",
                        icon_url=ctx.author.avatar_url,
                    )
                )
        except:
            await ctx.send(
                ":warning: | **An error has occured. Please report this to developer.**"
            )

    @commands.command()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def discrim(self, ctx, discrim=None):
        if discrim is None:
            try:
                await NaokoPaginator(
                    entries=[
                        user
                        for user in self.bot.users
                        if user.discriminator == ctx.author.discriminator
                    ],
                    colour=random.randint(0x000000, 0xFFFFFF),
                    title=f"Users with discriminator #{ctx.author.discriminator}",
                    length=5,
                    fmt="``",
                ).paginate(ctx)
            except:
                await ctx.send(
                    f":warning: | **No users found with discriminator #{ctx.author.discriminator} or it is invalid (ex. 0001)**",
                    delete_after=10,
                )
        else:
            try:
                await NaokoPaginator(
                    entries=[
                        user for user in self.bot.users if user.discriminator == discrim
                    ],
                    colour=random.randint(0x000000, 0xFFFFFF),
                    title=f"Users with discriminator #{discrim}",
                    length=5,
                    fmt="``",
                ).paginate(ctx)
            except:
                await ctx.send(
                    f":warning: | **No users found with discriminator #{discrim} or it is invalid (ex. 0001)**".replace(
                        "@", "@\u200b"
                    ),
                    delete_after=10,
                )

    @commands.command()
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def roles(self, ctx):
        """Shows all guild roles"""
        await NaokoPaginator(
            entries=[
                f"{r.mention}: **{len(r.members)}** member(s)"
                for r in ctx.guild.roles
                if r.name != "@everyone" and not r.managed
            ],
            colour=random.randint(0x000000, 0xFFFFFF),
            title=f"Roles of {ctx.guild}",
            length=5,
        ).paginate(ctx)

    @commands.command(name="roleinfo", aliases=["role-info", "rinfo"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def _role_info(self, ctx, *, role: discord.Role):
        """Shows information about a role"""
        await ctx.send(
            embed=discord.Embed(
                color=role.colour, title=role.name, timestamp=ctx.message.created_at
            )
            .add_field(
                name="**:spy: Role members:**",
                value=f"● **{len(role.members)}**",
                inline=True,
            )
            .add_field(
                name="**:paintbrush: Role colour:**",
                value=f"● **{role.colour}**",
                inline=True,
            )
            .add_field(
                name="**:clock10: Created at:**",
                value=f"● **{role.created_at}**",
                inline=True,
            )
            .add_field(
                name="**:arrow_heading_up: Position:**",
                value=f"● **{role.position}**",
                inline=True,
            )
            .add_field(
                name="**:ping_pong: Mentionable | Mention:**",
                value=f"● **{role.mentionable}** | **{role.mention}**",
                inline=True,
            )
            .add_field(
                name="**:space_invader: Managed:**",
                value=f"● **{role.managed}**",
                inline=True,
            )
            .set_thumbnail(
                url=f"https://via.placeholder.com/250x250/{str(role.colour).replace('#', '')}/{str(role.colour).replace('#', '')}"
            )
            .set_footer(
                text=f"{role.name} belongs to {ctx.guild}", icon_url=ctx.guild.icon_url
            )
        )

    @commands.command(aliases=["qr"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def qrcode(self, ctx, *, text: str):
        """Generates a QR-Code"""
        try:
            await ctx.send(
                embed=discord.Embed(
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at,
                )
                .set_image(
                    url=f"http://chart.apis.google.com/chart?cht=qr&chs=300x300&chl={quote(text)}&chld=H|0"
                )
                .set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            )
        except:
            pass

    @commands.command(aliases=["saucefinder"])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def sourcefinder(self, ctx, url: str):
        """Finds source of an image"""
        await ctx.send(
            embed=discord.Embed(color=random.randint(0x000000, 0xFFFFFF)).add_field(
                name="**Success!**",
                value=f"**[Click me for image source](https://www.google.com/searchbyimage?site=search&image_url={url})**",
            )
        )

    @commands.command(aliases=["backup"])
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def getdata(self, ctx, *, channel: discord.channel.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if channel.is_nsfw():
            await ctx.send(":warning: | **Can't get data from NSFW channel.**")
        else:
            loading = await ctx.send(
                f":information_source: | **Getting data from {channel.mention}...**"
            )
            try:
                async with self.session.post(
                    "https://hastebin.com/documents",
                    data="\n".join(
                        [
                            f"[{o.created_at}] {o.author}: {o.content} {' '.join([o.url for o in o.attachments])}"
                            async for o in channel.history(limit=1000)
                        ]
                    ).encode("utf-8"),
                ) as post:
                    post = await post.json()
                    await loading.edit(
                        content=f":white_check_mark: | **Uploaded: https://hastebin.com/{post['key']}**"
                    )
            except Excepion as e:
                await ctx.send(f":warning: | **Failed: `{e}`**")


def setup(bot):
    bot.add_cog(Fun(bot))
