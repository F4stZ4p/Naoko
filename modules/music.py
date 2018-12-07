import logging
import math
import re

import discord
from discord.ext import commands
import asyncio

import lavalink
import random
from utils.naoko_paginator import NaokoPaginator
from checks.naoko_checks import *

time_rx = re.compile("[0-9]+")
url_rx = re.compile("https?:\/\/(?:www\.)?.+")


class Equalizer:
    def __init__(self):
        self._band_count = 15
        self.bands = [0.0 for x in range(self._band_count)]
        self.freqs = [
            "25",
            "40",
            "63",
            "100",
            "160",
            "250",
            "400",
            "630",
            "1K",
            "1.6",
            "2.5",
            "4K",
            "6.3",
            "10K",
            "16K",
        ]

    def set_gain(self, band: int, gain: float):
        if band < 0 or band >= self._band_count:
            raise IndexError(f"Band {band} does not exist!")

        gain = min(max(gain, -0.25), 1.0)

        self.bands[band] = gain

    def get_gain(self, band: int):
        if band < 0 or band >= self._band_count:
            raise IndexError(f"Band {band} does not exist!")

        return self.bands[band]

    def visualise(self):
        block = ""
        bands = [f"{self.freqs[band]:>3}" for band in range(self._band_count)]
        bottom = (" " * 8) + "  ".join(bands)

        gains = [
            1.0,
            0.9,
            0.8,
            0.7,
            0.6,
            0.5,
            0.4,
            0.3,
            0.2,
            0.1,
            0.0,
            -0.1,
            -0.2,
            -0.25,
        ]

        for gain in gains:
            prefix = " "

            if gain > 0:
                prefix = "+"
            elif gain == 0:
                prefix = " "
            else:
                prefix = ""

            block += f"{prefix}{gain:.2f} | "

            for value in self.bands:
                if value >= gain:
                    block += "▄▄▄  "
                else:
                    block += "     "

            block += "\n"

        block += bottom
        return block


class Music:
    """Music-related module"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/O2CKXgN.png"
        self.bot.lavalink.register_hook(self._track_hook)

    def __unload(self):
        self.bot.loop.create_task(self.bot.lavalink.players.safe_clear())
        self.bot.lavalink.unregister_hook(self._track_hook)

    async def _track_hook(self, event):
        if not hasattr(event, "player"):
            return
        channel = self.bot.get_channel(event.player.fetch("channel"))
        if not channel:
            return

        if isinstance(event, lavalink.Events.TrackStartEvent):
            req = self.bot.get_user(event.track.requester)
            await channel.send(
                embed=discord.Embed(
                    title="Now playing:",
                    description=event.track.title,
                    color=random.randint(0x000000, 0xFFFFFF),
                )
                .set_thumbnail(
                    url=f"https://img.youtube.com/vi/{event.track.identifier}/hqdefault.jpg"
                )
                .set_footer(
                    icon_url=req.avatar_url, text=f"Track requested by {req.name}"
                )
            )

        elif isinstance(event, lavalink.Events.QueueEndEvent):
            await channel.send("Queue ended! Leaving due to inactivity...")
            await event.player.disconnect()

    async def get_player(self, guild, create: bool = True):
        return await self.bot.lavalink.get_player(guild.id, create)

    @commands.command()
    async def eq(self, ctx):
        player = await self.bot.lavalink.get_player(ctx.guild.id)
        eq = player.fetch("eq", Equalizer())

        reactions = ["◀", "⬅", "⏫", "🔼", "🔽", "⏬", "➡", "▶", "⏺"]

        veq = await ctx.send(f"```fix\n{eq.visualise()}```")
        for reaction in reactions:
            await veq.add_reaction(reaction)

        await self.interact(ctx, player, eq, veq, 0)

    async def interact(self, ctx, player, eq, m, selected):
        player.store("eq", eq)
        selector = f'{" " * 8}{"     " * selected}^^^'
        await m.edit(content=f"```fix\n{eq.visualise()}\n{selector}```")

        reaction = await self.get_reaction(ctx, m.id)

        if not reaction:
            try:
                await m.clear_reactions()
            except discord.Forbidden:
                pass
        elif reaction == "⬅":
            await self.interact(ctx, player, eq, m, max(selected - 1, 0))
        elif reaction == "➡":
            await self.interact(ctx, player, eq, m, min(selected + 1, 14))
        elif reaction == "🔼":
            gain = min(eq.get_gain(selected) + 0.1, 1.0)
            eq.set_gain(selected, gain)
            await self.apply_gain(ctx.guild.id, selected, gain)
            await self.interact(ctx, player, eq, m, selected)
        elif reaction == "🔽":
            gain = max(eq.get_gain(selected) - 0.1, -0.25)
            eq.set_gain(selected, gain)
            await self.apply_gain(ctx.guild.id, selected, gain)
            await self.interact(ctx, player, eq, m, selected)
        elif reaction == "⏫":
            gain = 1.0
            eq.set_gain(selected, gain)
            await self.apply_gain(ctx.guild.id, selected, gain)
            await self.interact(ctx, player, eq, m, selected)
        elif reaction == "⏬":
            gain = -0.25
            eq.set_gain(selected, gain)
            await self.apply_gain(ctx.guild.id, selected, gain)
            await self.interact(ctx, player, eq, m, selected)
        elif reaction == "◀":
            selected = 0
            await self.interact(ctx, player, eq, m, selected)
        elif reaction == "▶":
            selected = 14
            await self.interact(ctx, player, eq, m, selected)
        elif reaction == "⏺":
            for band in range(eq._band_count):
                eq.set_gain(band, 0.0)

            await self.apply_gains(ctx.guild.id, eq.bands)
            await self.interact(ctx, player, eq, m, selected)

    async def apply_gain(self, guild_id, band, gain):
        await self.apply_gains(guild_id, {"band": band, "gain": gain})

    async def apply_gains(self, guild_id, gains):
        payload = {"op": "equalizer", "guildId": str(guild_id)}

        if isinstance(gains, list):
            payload["bands"] = [{"band": x, "gain": y} for x, y in enumerate(gains)]
        elif isinstance(gains, dict):
            payload["bands"] = [gains]

        player = await self.bot.lavalink.get_player(int(guild_id))
        await player.node.ws.send(**payload)

    async def get_reaction(self, ctx, m_id):
        reactions = ["◀", "⬅", "⏫", "🔼", "🔽", "⏬", "➡", "▶", "⏺"]

        def check(r, u):
            return (
                r.message.id == m_id and u.id == ctx.author.id and r.emoji in reactions
            )

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", check=check, timeout=20
            )
        except asyncio.TimeoutError:
            return None
        else:
            try:
                await reaction.message.remove_reaction(reaction.emoji, user)
            except discord.Forbidden:
                pass
            return reaction.emoji

    async def get_reaction(self, ctx, m_id):
        reactions = ["◀", "⬅", "⏫", "🔼", "🔽", "⏬", "➡", "▶", "⏺"]

        def check(r, u):
            return (
                r.message.id == m_id and u.id == ctx.author.id and r.emoji in reactions
            )

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", check=check, timeout=20
            )
        except asyncio.TimeoutError:
            return None
        else:
            try:
                await reaction.message.remove_reaction(reaction.emoji, user)
            except discord.Forbidden:
                pass
            return reaction.emoji

    @commands.command(name="play", aliases=["p"])
    @commands.guild_only()
    async def _play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        async with ctx.typing():
            player = await self.get_player(ctx.guild)

            query = query.strip("<>")

            if not url_rx.match(query):
                query = f"ytsearch:{query}"

            results = await self.bot.lavalink.get_tracks(query)

            if not results or (isinstance(results, dict) and not results["tracks"]):
                return await ctx.send("Nothing found!")

            if isinstance(results, dict):
                tracks = results["tracks"]
                if results["loadType"] == "PLAYLIST_LOADED":
                    await self.queue_playlist(
                        player, tracks, ctx.channel, ctx.author, results["playlistInfo"]
                    )
                else:
                    if (
                        tracks[0]["info"]["length"] > 18_000_000
                        and ctx.author.id not in self.bot.patrons
                    ):
                        return await ctx.send(
                            embed=discord.Embed(
                                title="Naoko PRO",
                                color=random.randint(0x000000, 0xFFFFFF),
                                description="Can't enqueue songs which are longer than 5 hours\nIf you want to, then donate and get **PRO** - **live** and **unlimited** tracks, **playnow**, **repeat** commands and more!\n\n**[Click me!](https://patreon.com/F4stZ4p)**",
                                timestamp=ctx.message.created_at,
                            )
                            .set_footer(
                                text=ctx.author.name, icon_url=ctx.author.avatar_url
                            )
                            .set_thumbnail(url=self.thumbnail)
                        )
                    await self.queue_song(player, tracks, ctx.channel, ctx.author)
            else:
                if "list" in query and "ytsearch:" not in query:
                    await self.queue_playlist(player, results, ctx.channel, ctx.author)
                else:
                    if (
                        results[0]["info"]["length"] > 18_000_000
                        and ctx.author.id not in self.bot.patrons
                    ):
                        return await ctx.send(
                            embed=discord.Embed(
                                title="Naoko PRO",
                                color=random.randint(0x000000, 0xFFFFFF),
                                description="Can't enqueue songs which are longer than 5 hours\nIf you want to, then donate and get **PRO** - **live** and **unlimited** tracks, **playnow**, **repeat** commands and more!\n\n**[Click me!](https://patreon.com/F4stZ4p)**",
                                timestamp=ctx.message.created_at,
                            )
                            .set_footer(
                                text=ctx.author.name, icon_url=ctx.author.avatar_url
                            )
                            .set_thumbnail(url=self.thumbnail)
                        )
                    await self.queue_song(player, results, ctx.channel, ctx.author)

            if not player.is_playing:
                await player.play()

    async def queue_song(self, player, tracks, channel, author):
        track = tracks[0]
        track_title = track["info"]["title"]
        track_uri = track["info"]["uri"]
        embed = discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
        embed.title = "Track enqueued!"
        embed.set_thumbnail(
            url=f'https://img.youtube.com/vi/{track["info"]["identifier"]}/hqdefault.jpg'
        )
        embed.description = f"[{track_title}]({track_uri})"
        await channel.send(embed=embed)
        player.add(requester=author.id, track=track)

    async def queue_playlist(self, player, tracks, channel, author, info: bool = False):
        embed = discord.Embed(color=discord.Color.blurple())
        for track in tracks:
            player.add(requester=author.id, track=track)

        embed.title = "Playlist enqueued!"
        if info:
            embed.description = f'{info["name"]} - {len(tracks)} tracks'
        else:
            embed.description = f"Imported **{len(tracks)}** tracks from the playlist!"
        await channel.send(embed=embed)

    @commands.command(name="previous", aliases=["pv"])
    @commands.guild_only()
    async def _previous(self, ctx):
        """ Plays the previous song. """
        player = await self.get_player(ctx.guild)

        try:
            await player.play_previous()
        except lavalink.NoPreviousTrack:
            await ctx.send(
                ":warning: | **There is no previous song to play**", delete_after=5
            )

    @commands.command(name="playnow", aliases=["pn"])
    @commands.guild_only()
    @patron()
    async def _playnow(self, ctx, *, query: str):
        """ Plays immediately a song. """
        async with ctx.typing():
            player = await self.get_player(ctx.guild)

            if not player.queue and not player.is_playing:
                return await ctx.invoke(self._play, query=query)

            query = query.strip("<>")

            if not url_rx.match(query):
                query = f"ytsearch:{query}"

            results = await self.bot.lavalink.get_tracks(query)

            if not results or (isinstance(results, dict) and not results["tracks"]):
                return await ctx.send("Nothing found!")

            if isinstance(results, dict):
                track = results["tracks"].pop(0)
                if results["loadType"] == "PLAYLIST_LOADED":
                    await self.queue_playlist(
                        player,
                        results["tracks"],
                        ctx.channel,
                        ctx.author,
                        results["playlistInfo"],
                    )
            else:
                track = results.pop(0)
                if "list" in query and "ytsearch:" not in query:
                    await self.queue_playlist(player, results, ctx.channel, ctx.author)

            await player.play_now(requester=ctx.author.id, track=track)

    @commands.command(name="playat", aliases=["pa"])
    @commands.guild_only()
    async def _playat(self, ctx, index: int):
        """ Plays the queue from a specific point. Disregards tracks before the index. """
        player = await self.get_player(ctx.guild)

        if index < 1:
            return await ctx.send("Invalid specified index.")

        if len(player.queue) < index:
            return await ctx.send("This index exceeds the queue's length.")

        await player.play_at(index - 1)

    @commands.command(name="seek")
    @commands.guild_only()
    async def _seek(self, ctx, *, time: str):
        """ Seeks to a given position in a track. """
        player = await self.get_player(ctx.guild)

        if not player.is_playing:
            return await ctx.send("Not playing.")

        seconds = time_rx.search(time)
        if not seconds:
            return await ctx.send("You need to specify the amount of seconds to skip!")

        seconds = int(seconds.group()) * 1000
        if time.startswith("-"):
            seconds *= -1

        track_time = player.position + seconds
        await player.seek(track_time)

        await ctx.send(f"Moved track to **{lavalink.Utils.format_time(track_time)}**")

    @commands.command(name="skip", aliases=["forceskip", "fs"])
    @commands.guild_only()
    async def _skip(self, ctx):
        """ Skips the current track. """
        player = await self.get_player(ctx.guild)

        if not player.is_playing:
            return await ctx.send(":warning: | **Not playing**", delete_after=5)

        await player.skip()
        await ctx.send("⏭ | **Skipped**", delete_after=5)

    @commands.command(name="stop")
    @commands.guild_only()
    async def _stop(self, ctx):
        """ Stops the player and clears its queue. """
        player = await self.get_player(ctx.guild)

        if not player.is_playing:
            return await ctx.send(":warning: | **Not playing**", delete_after=5)

        player.queue.clear()
        await player.stop()
        await ctx.send("⏹ | **Stopped**", delete_after=5)

    @commands.command(name="now", aliases=["np", "n", "playing"])
    @commands.guild_only()
    async def _now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = await self.get_player(ctx.guild)
        song = "Nothing"

        if player.current:
            position = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                duration = "🔴 LIVE"
            else:
                duration = lavalink.Utils.format_time(player.current.duration)
            song = f"**[{player.current.title}]({player.current.uri})**\n({position}/{duration})"

        embed = discord.Embed(
            color=discord.Color.blurple(), title="Now Playing", description=song
        )
        await ctx.send(embed=embed)

    @commands.command(name="queue", aliases=["q"])
    @commands.guild_only()
    async def _queue(self, ctx):
        """ Shows the player's queue. """
        player = await self.get_player(ctx.guild)

        if not player.queue:
            return await ctx.send(
                ":information_source: | **The queue is empty now. Go and queue something :smiley:**",
                delete_after=10,
            )

        await NaokoPaginator(
            title=f"{ctx.guild.name} Music Queue",
            length=5,
            colour=random.randint(0x000000, 0xFFFFFF),
            entries=[
                f"`{index + 1}` - [**{track.title}**]({track.uri})"
                for index, track in enumerate(player.queue)
            ],
        ).paginate(ctx)

    @commands.command(name="pause", aliases=["resume"])
    @commands.guild_only()
    async def _pause(self, ctx):
        """ Pauses/Resumes the current track. """
        player = await self.get_player(ctx.guild)

        if not player.is_playing:
            return await ctx.send(":warning: | **Not playing**", delete_after=5)

        if player.paused:
            await player.set_pause(False)
            await ctx.send("⏯ | **Resumed**", delete_after=5)
        else:
            await player.set_pause(True)
            await ctx.send("⏯ | **Paused**", delete_after=5)

    @commands.command(name="volume", aliases=["vol"])
    @commands.guild_only()
    async def _volume(self, ctx, volume: int = None):
        """ Changes the player's volume. Must be between 0 and 1000"""
        player = await self.get_player(ctx.guild)

        if not volume:
            return await ctx.send(f"🔈 | **{player.volume}%**")

        await player.set_volume(volume)
        await ctx.send(f"🔈 | **Set to {player.volume}%**")

    @commands.command(name="bassboost", aliases=["bb"])
    async def _bassboost(self, ctx, level: str = None):
        """ Changes the player's bass frequencies up to 4 levels. OFF, LOW, MEDIUM, HIGH, INSANE and ULTRA"""
        player = await self.get_player(ctx.guild)

        levels = {
            "OFF": [(0, 0), (1, 0)],
            "LOW": [(0, 0.25), (1, 0.15)],
            "MEDIUM": [(0, 0.50), (1, 0.25)],
            "HIGH": [(0, 0.75), (1, 0.50)],
            "INSANE": [(0, 1), (1, 0.75)],
            "ULTRA": [(0, 1), (1, 2.0)],
        }

        if not level:
            for k, v in levels.items():
                if [(0, player.equalizer[0]), (1, player.equalizer[1])] == v:
                    level = k
                    break
            return await ctx.send(
                "Bass boost currently set on `{}`.".format(level if level else "CUSTOM")
            )

        gain = None

        for k in levels.keys():
            if k.startswith(level.upper()):
                gain = levels[k]
                break

        if not gain:
            return await ctx.send(":warning: | **Invalid level**", delete_after=5)

        await player.set_gains(*gain)

        await ctx.send(
            f":information_source: | **Bass Boost is now `{k}`**", delete_after=5
        )

    @commands.command(name="shuffle")
    @commands.guild_only()
    async def _shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = await self.get_player(ctx.guild)
        if not player.is_playing:
            return await ctx.send(":warning: | **Nothing playing**", delete_after=5)

        player.shuffle = not player.shuffle
        await ctx.send(f"🔀 | **Shuffle {'enabled' if player.shuffle else 'disabled'}**")

    @commands.command(name="repeat", aliases=["loop"])
    @commands.guild_only()
    @patron()
    async def _repeat(self, ctx):
        """ Repeats the current song until the command is invoked again. """
        player = await self.get_player(ctx.guild)

        if not player.is_playing:
            return await ctx.send(":warning: | **Nothing playing**", delete_after=5)

        player.repeat = not player.repeat
        await ctx.send(
            f"🔁 | **Repeat {'enabled' if player.repeat else 'disabled'}**",
            delete_after=5,
        )

    @commands.command(name="remove")
    @commands.guild_only()
    async def _remove(self, ctx, index: int):
        """ Removes an item from the player's queue with the given index. """
        player = await self.get_player(ctx.guild)

        if not player.queue:
            return await ctx.send(":warning: | **Nothing queued**", delete_after=5)

        if index > len(player.queue) or index < 1:
            return await ctx.send(
                f":warning: | **Index has to be between 1 and {len(player.queue)}**",
                delete_after=15,
            )

        index -= 1
        removed = player.queue.pop(index)

        await ctx.send(f"Removed **{removed.title}** from the queue.")

    @commands.command(name="find")
    @commands.guild_only()
    async def _find(self, ctx, *, query):
        """ Lists the first 10 search results from a given query. """
        if not query.startswith("ytsearch:") and not query.startswith("scsearch:"):
            query = "ytsearch:" + query

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results["tracks"]:
            return await ctx.send(":warning: | **Nothing found**", delete_after=5)

        tracks = results["tracks"][:10]  # First 10 results

        o = ""
        for index, track in enumerate(tracks, start=1):
            track_title = track["info"]["title"]
            track_uri = track["info"]["uri"]

            o += f"`{index}.` [{track_title}]({track_uri})\n"

        embed = discord.Embed(color=discord.Color.blurple(), description=o)
        await ctx.send(embed=embed)

    @commands.command(name="disconnect", aliases=["dc"])
    @commands.guild_only()
    async def _disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = await self.get_player(ctx.guild)

        if not player.is_connected:
            return await ctx.send(":warning: | **Not connected**", delete_after=5)

        if not ctx.author.voice or (
            player.is_connected
            and ctx.author.voice.channel.id != int(player.channel_id)
        ):
            return await ctx.send("You're not in my voicechannel!")

        player.queue.clear()
        await player.disconnect()
        await ctx.send("*⃣ | **Disconnected**", delete_after=5)

    @_playnow.before_invoke
    @_previous.before_invoke
    @_play.before_invoke
    async def ensure_voice(self, ctx):
        """ A few checks to make sure the bot can join a voice channel. """
        player = await self.get_player(ctx.guild)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                await ctx.send("You aren't connected to any voice channel.")
                raise commands.CommandInvokeError(
                    "Author not connected to voice channel."
                )

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                await ctx.send("Missing permissions `CONNECT` and/or `SPEAK`.")
                raise commands.CommandInvokeError(
                    "Bot has no permissions CONNECT and/or SPEAK"
                )

            player.store("channel", ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
        else:
            if player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send("Join my voice channel!")


def setup(bot):
    bot.add_cog(Music(bot))
