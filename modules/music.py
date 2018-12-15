import discord
import aqualink
from discord.ext import commands
from datetime import timedelta


class Music:
    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/O2CKXgN.png"
        self.queue = {}
    
    async def track_callback(self, player):
        """A callback invoked when the song is done playing."""
        queue_data = self.queue[player.guild]  # get the queue data
        if not queue_data[1]:  # no more songs left
            await player.disconnect()  # stop the player
        else:
            track = queue_data[1].pop(0)  # get the next song
            await player.play(track)  # play it
            await queue_data[0].send(f"Playing {track.title}")

    @commands.command()
    async def play(self, ctx, *, query: str):
        """Queue a song."""
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not ctx.guild.me.voice:
            await player.connect(ctx.author.voice.channel.id)
        tracks = await player.query(f"ytsearch: {query}")
        track = tracks[0]
        if self.queue.get(ctx.guild):
            self.queue[ctx.guild][1].append(track)
            await ctx.send(f"Added {track.title} to the queue")
        else:
            self.queue[ctx.guild] = [ctx.channel, []]
            await player.play(track) # plays the track
            await ctx.send(f"Playing {track.title}")
        player.track_callback = self.track_callback  # set an event for track end

    @commands.command()
    async def skip(self, ctx):
        """Skip the current song."""
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if player.paused or player.playing:
            await player.stop()
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("I'm not playing...")

    @commands.command(name="queue", aliases=["q"])
    async def _queue(self, ctx):
        """Shows up to 5 queued songs."""
        player = self.bot.aqualink.get_player(ctx.guild.id)
        queue = self.queue.get(ctx.guild)
        if not queue:
            return await ctx.send("I am not playing at all.")
        queue = queue[1][:5]
        if not queue:
            return await ctx.send("No more upcoming tracks...")
        queue_text = "\n".join(f"{t.title} by {t.author}" for t in queue)
        await ctx.send(queue_text)

    @commands.command(aliases=["np"])
    async def now_playing(self, ctx):
        """Show the currently playing song."""
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not player.track:
            return await ctx.send("I'm not playing anything.")
        track = player.track
        em = discord.Embed(title=f"Playing in {ctx.guild}")
        em.add_field(name="Track", value=track.title)
        em.add_field(name="Author", value=track.author)
        em.add_field(name="Length", value=str(timedelta(milliseconds=track.length)))
        em.add_field(name="Position", value=str(timedelta(milliseconds=track.position)))
        em.add_field(name="Volume", value=f"{player.volume}%")
        em.set_thumbnail(url=track.thumbnail)
        await ctx.send(embed=em)

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, vol: int):
        """Sets the volume."""
        if vol < 0 or vol > 150:
            return await ctx.send(
                "Must be smaller than 151 and bigger than or equal to 0."
            )
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not player.playing:
            return await ctx.send("I'm not playing!")
        await player.set_volume(vol)
        await ctx.send(f"Volume set to {vol}%")

    @commands.command()
    async def stop(self, ctx):
        """Stop the fun."""
        player = self.bot.aqualink.get_player(ctx.guild.id)
        if not player.connected or not ctx.guild.me.voice:
            return await ctx.send("I'm not playing.")
        player.track_callback = None  # prevent unusual behavior
        await player.stop()
        await player.disconnect()
        await ctx.send("Stopped.")


def setup(bot):
    bot.add_cog(Music(bot))
