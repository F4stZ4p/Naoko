import discord
import random
from discord.ext import commands
from utils.naoko_paginator import NaokoPaginator
from urllib.parse import quote


class Search:
    """Search anything you want~"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/rKFyFCL.png"

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def search(self, ctx):
        """Search something (anime, manga, lyrics, wikipedia)"""
        await ctx.send(
            ":information_source: | **Please provide what to search (anime, manga, lyrics, wikipedia)**"
        )

    @search.command()
    async def anime(self, ctx, *, query: str):
        """Shows you information about anime"""
        async with ctx.typing():
            try:
                async with self.bot.session.get(
                    f"https://api.jikan.moe/search/anime/{query}"
                ) as resp:
                    data = await resp.json()
                    embed = discord.Embed(
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                        title=data["result"][0].get("title"),
                    )
                    embed.add_field(
                        name=":gem: Short description:",
                        value=f"{data['result'][0].get('description')}**[Read more about {data['result'][0].get('title')}...]({data['result'][0].get('url')})**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":clapper: Episodes:",
                        value=f"**{data['result'][0].get('episodes')}**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":heart_decoration: MyAnimeList rating:",
                        value=f"**{data['result'][0].get('score')}/10**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":busts_in_silhouette: Members:",
                        value=f"**{data['result'][0].get('members')}**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":performing_arts: Type:",
                        value=f"**{data['result'][0].get('type')}**",
                        inline=True,
                    )
                    embed.set_thumbnail(url=data["result"][0].get("image_url"))
                    embed.set_footer(
                        text=f"Anime search for - {query}",
                        icon_url=ctx.author.avatar_url,
                    )
                    await ctx.send(embed=embed)
            except BaseException:
                await ctx.send(f":warning: | **No results found for ``{query}``**")

    @search.command()
    async def manga(self, ctx, *, query: str):
        """Shows you information about manga"""
        async with ctx.typing():
            try:
                async with self.bot.session.get(
                    f"https://api.jikan.moe/search/manga/{query}"
                ) as resp:
                    data = await resp.json()
                    embed = discord.Embed(
                        color=random.randint(0x000000, 0xFFFFFF),
                        timestamp=ctx.message.created_at,
                        title=data["result"][0].get("title"),
                    )
                    embed.add_field(
                        name=":gem: Short description:",
                        value=f"{data['result'][0].get('description')}**[Read more about {data['result'][0].get('title')}...]({data['result'][0].get('url')})**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":clapper: Volumes:",
                        value=f"**{data['result'][0].get('volumes')}**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":heart_decoration: MyAnimeList rating:",
                        value=f"**{data['result'][0].get('score')}/10**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":busts_in_silhouette: Members:",
                        value=f"**{data['result'][0].get('members')}**",
                        inline=True,
                    )
                    embed.add_field(
                        name=":performing_arts: Type:",
                        value=f"**{data['result'][0].get('type')}**",
                        inline=True,
                    )
                    embed.set_thumbnail(url=data["result"][0].get("image_url"))
                    embed.set_footer(
                        text=f"Manga search for - {query}",
                        icon_url=ctx.author.avatar_url,
                    )
                    await ctx.send(embed=embed)
            except BaseException:
                await ctx.send(f":warning: | **No results found for ``{query}``**")

    @search.command()
    async def lyrics(self, ctx, artist: str, *, song: str):
        """Reveals a lyrics text for a song"""
        async with ctx.typing():
            try:
                try:
                    async with self.bot.session.get(
                        f"https://orion.apiseeds.com/api/music/lyric/{artist}/{song}?apikey={self.lyricskey}"
                    ) as resp:
                        data = await resp.json()
                        await ctx.send(
                            embed=discord.Embed(
                                color=random.randint(0x000000, 0xFFFFFF)
                            ).add_field(
                                name=":page_facing_up: Lyrics text",
                                value=f"```fix\n{data['result']['track'].get('text')}```",
                            )
                        )

                except discord.errors.HTTPException:
                    await ctx.send(
                        ":information_source: | **Looks like lyrics are very long. Trying upload to hastebin.**"
                    )
                    try:
                        async with self.bot.session.post(
                            "https://hastebin.com/documents",
                            data=data["result"]["track"].get("text").encode("utf-8"),
                        ) as post:
                            post = await post.json()
                            await ctx.send(
                                f':white_check_mark: | **Uploaded. URL: https://hastebin.com/{post["key"]}**'
                            )
                    except BaseException:
                        await ctx.send(
                            ":warning: | **Uploading to hastebin failed. Please report this issue to developer.**"
                        )
            except BaseException:
                await ctx.send(
                    f":warning: | **No results found for ``{artist}`` - ``{song}``**"
                )

    @search.command()
    async def wikipedia(self, ctx, search: str, language: str = "en"):
        """Lets you search Wikipedia.
        For example, n.search wikipedia "cucumber" en
        Will give you definition of cucumber in english. Default language is english so you can just n.search wikipedia "cucumber"
        If you want to search in other language, for example word cucumber in russian (огурец), you need to specify language:
        n.search wikipedia "огурец" ru
        This will give you definition of word cucumber in russian.
        """
        async with ctx.typing():
            try:
                async with self.bot.session.get(
                    f"https://{language.lower()}.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={search}&redirects=1&indexpageids"
                ) as resp:
                    data = await resp.json()
            except BaseException:
                await ctx.send(
                    f":warning: | **Invalid language provided (`{language.lower()}`). Example: ru - Russian; en - English**"
                )
            if (data["query"]["pages"][data["query"]
                                       ["pageids"][0]].get("extract") is None):
                await ctx.send(
                    f":warning: | **No results found for `{search}` in `{language}` language.**"
                )
            else:
                try:
                    await ctx.send(
                        embed=discord.Embed(
                            color=random.randint(0x000000, 0xFFFFFF),
                            title=f"Wikipedia search - {search}",
                        )
                        .add_field(
                            name=f":satellite_orbital: Found - {data['query']['pages'][data['query']['pageids'][0]].get('title')}",
                            value=f"```fix\n{data['query']['pages'][data['query']['pageids'][0]].get('extract')}```",
                        )
                        .set_footer(
                            text=f"Wikipedia search by: {ctx.author}",
                            icon_url=ctx.author.avatar_url,
                        )
                    )
                except discord.errors.HTTPException:
                    await ctx.send(
                        ":information_source: | **Looks like text is too long. Trying upload to hastebin.**"
                    )
                    try:
                        async with self.bot.session.post(
                            "https://hastebin.com/documents",
                            data=f"Naoko Wikipedia Search - {search} | Language: {language.lower()}\nFound: {data['query']['pages'][data['query']['pageids'][0]].get('title')}\nText: {data['query']['pages'][data['query']['pageids'][0]].get('extract')}".encode(
                                "utf-8"
                            ),
                        ) as post:
                            post = await post.json()
                            await ctx.send(
                                f':white_check_mark: | **Uploaded. URL: https://hastebin.com/{post["key"]}**'
                            )
                    except BaseException:
                        await ctx.send(
                            ":warning: | **Uploading to hastebin failed. Please report this issue to developer.**"
                        )

    @search.command(aliases=["ddg", "web"])
    @commands.cooldown(1.0, 30.0, commands.BucketType.user)
    async def duckduckgo(self, ctx, *, query: str):
        """DuckDuckGo Search"""
        await ctx.trigger_typing()
        res = await self.bot.session.get(
            "https://api.duckduckgo.com",
            params={
                "q": quote(query),
                "t": "Naoko Discord Bot",
                "format": "json",
                "no_html": "1",
            },
        )

        resp_json = await res.json(content_type="application/x-javascript")

        embeds = {}

        if resp_json["AbstractURL"] != "":
            embeds[f'Abstract: {resp_json["Heading"]}'
                   f' ({resp_json["AbstractSource"]})'] = {"image": resp_json["Image"],
                                                           "desc": f'{resp_json.get("AbstractText", "")}\n\n'
                                                           f'{resp_json["AbstractURL"]}',
                                                           }

        if resp_json["Definition"] != "":
            embeds["Definition"] = {
                "desc": f'{resp_json["Definition"]}\n'
                f'([{resp_json["DefinitionSource"]}]'
                f'({resp_json["DefinitionURL"]}))'
            }

        if resp_json["RelatedTopics"]:
            desc = []
            for topic in resp_json["RelatedTopics"]:
                try:
                    if len("\n".join(desc)) > 1000:
                        break
                    desc.append(f'[**{topic["Text"]}**]({topic["FirstURL"]})')
                except KeyError:
                    continue

            embeds["Related"] = {
                "desc": "\n".join(desc),
                "image": resp_json["RelatedTopics"][0]["Icon"]["URL"],
            }

        if resp_json["Results"]:
            desc = []
            for result in resp_json["Results"]:
                desc.append(f'[**{result["Text"]}**]({result["FirstURL"]})')
            embeds["Top Results"] = {
                "desc": "\n".join(desc),
                "image": resp_json["Results"][0]["Icon"]["URL"],
            }

        final_embeds = []

        for embed_title, embed_content in embeds.items():
            final_embeds.append(
                discord.Embed(
                    title=embed_title,
                    description=embed_content["desc"],
                    color=random.randint(0x000000, 0xFFFFFF),
                )
                .set_image(url=embed_content["image"])
                .set_thumbnail(url="https://i.imgur.com/cD6Xn0W.png")
            )

        if not final_embeds:
            return await ctx.send(
                ":information_source: | **Sorry, no results found**", delete_after=5
            )

        await NaokoPaginator(extras=final_embeds).paginate(ctx)


def setup(bot):
    bot.add_cog(Search(bot))
