import discord, asyncio, re, os, psutil, traceback, time, gc, random, aiohttp, asyncpg, sys, lavalink
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import utils.naoko_logger as logger
from utils.naoko_shell import shell
from config.naoko_config import NaokoConfig

try:
    import uvloop
except ImportError:
    pass
else:
    if sys.platform == "linux" and sys.version_info >= (3, 5):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Naoko(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix, case_insensitive=True)

        self.lavalink = lavalink.Client(bot=self, loop=self.loop)
        self.lavalink.nodes.add(lavalink.Regions.all(), password="adrianisgay12345", rest_port=2333, ws_port=80, host='127.0.0.1')

        self.config = NaokoConfig()
        self.blacklist = [entry for entry in self.config.blacklist]
        self.whitelist = [entry for entry in self.config.whitelist]
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.patrons = []
        self.launch_time = datetime.utcnow()
        self.startup_extensions = (
            "modules.snipes",
            "modules.image",
            "modules.events",
            "modules.minecraft",
            "modules.search",
            "modules.space",
            "modules.games",
            "modules.commands",
            "modules.misc",
            "modules.eh",
            "modules.fun",
            "modules.moderator",
            "modules.owner",
            "modules.economy",
            "modules.settings",
            "modules.customcommands",
            "modules.nsfw",
        )
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.stat = "No recent updates or announcements"
        self.all_prefixes = {}
        self.usage = {}

    async def get_prefix(self, message):
        if not message.guild:
            return commands.when_mentioned_or("n.")(self, message)
        try:
            return commands.when_mentioned_or(
                self.all_prefixes[message.guild.id], "n."
            )(self, message)
        except:
            return commands.when_mentioned_or("n.")(self, message)

    def __repr__(self):
        return "Naoko Bot"

    async def start_db(self):
        self.db = await asyncpg.create_pool(
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            host=self.config.host,
        )

    async def make_db(self):
        async with self.db.acquire() as con:
            await con.execute(
                "CREATE TABLE IF NOT EXISTS users(ID bigint, MONEY bigint)"
            )
            await con.execute(
                "CREATE TABLE IF NOT EXISTS prefix(GUILDID bigint, PREFIX varchar)"
            )
            await con.execute(
                'CREATE TABLE IF NOT EXISTS customcommands("guildid" bigint, "name" character varying(50), "action" character varying(3000));'
            )
            await con.execute("CREATE TABLE IF NOT EXISTS patrons(ID bigint);")
            await con.execute(
                "CREATE TABLE IF NOT EXISTS cars(ID bigint, car character varying(150));"
            )
        await self.db.release(con)

    async def _fetch_latest_commit(self):
        self.stat = await self.loop.run_in_executor(
            None, shell, 'git show -n 1 -s --format="[%h] %s"'
        )

    async def load_prefixes(self):
        async with self.db.acquire() as con:
            prefixes = await con.fetch("SELECT GUILDID, PREFIX FROM prefix;")
            for row in prefixes:
                self.all_prefixes[row[0]] = row[1]
            await self.db.release(con)

    async def load_patrons(self):
        async with self.db.acquire() as con:
            patrons = await con.fetch("SELECT * FROM patrons;")
            for row in patrons:
                self.patrons.append(row[0])
            await self.db.release(con)

    async def _get_owner(self):
        self.owner = (await self.application_info()).owner

    async def on_ready(self):
        self.loop.create_task(self.presence())
        logger.superlog(f"[ INFO ] Ready", f"On {len(self.guilds)} servers")

        await self._get_owner()
        await self.start_db()
        await self.load_prefixes()
        await self.load_patrons()
        await self._fetch_latest_commit()

    async def on_command(self, ctx):
        if ctx.author.id in self.patrons:
            ctx.command.reset_cooldown(ctx)

        try:
            self.usage[ctx.command.name] += 1
        except:
            self.usage[ctx.command.name] = 1

        logger.superlog(
            f"[ COMMAND ] {ctx.author}: {ctx.message.content}", ctx.message.guild
        )

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in self.blacklist:
            return

        else:
            if message.guild:
                try:
                    if (
                        message.content
                        in self.cogs["CustomCommands"].commands[message.guild.id]
                    ):
                        await message.channel.send(
                            self.cogs["CustomCommands"].commands[message.guild.id][
                                message.content
                            ]
                        )
                except:
                    pass

        await self.process_commands(message)

    async def presence(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await self.change_presence(
                status=discord.Status.dnd,
                activity=discord.Streaming(
                    name=random.choice(
                        (
                            "@Naoko help | naokobot.github.io",
                            f"{len(self.guilds)} guilds",
                            f"{len(self.users)} users",
                            f"{len(self.shards)} shard(s)",
                            f"{len(self.emojis)} emotes :kappa:",
                            "discord.io/naoko",
                        )
                    ),
                    url="https://twitch.tv/streamer",
                ),
            )
            await asyncio.sleep(35)

    def run(self):
        self.remove_command("help")
        for extension in self.startup_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(e)
        super().run(self.config.token, reconnect=True)


if __name__ == "__main__":
    Naoko().run()
