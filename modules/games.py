import discord
import asyncio
import random
from discord.ext import commands


class TicTacToe:
    def __init__(self, ctx):
        self.ctx = ctx
        self.x = "❌"
        self.o = "⭕"
        self.blank = "<:square:482175022278901770>"
        self.possible = {}
        self.whoturns = {}

        self.player_sign = self.x
        self.bot_sign = self.o

        self.field = [
            self.blank,
            self.blank,
            self.blank,
            self.blank,
            self.blank,
            self.blank,
            self.blank,
            self.blank,
            self.blank,
        ]

        self.buttons = {
            "1\u20e3": "1",
            "2\u20e3": "2",
            "3\u20e3": "3",
            "4\u20e3": "4",
            "5\u20e3": "5",
            "6\u20e3": "6",
            "7\u20e3": "7",
            "8\u20e3": "8",
            "9\u20e3": "9",
            "⏹": "stop",
        }

    def make_move(self, field, playerone):
        if self.whoturns[self.ctx.channel.id] == playerone.id:
            self.field[field] = self.player_sign
        else:
            self.field[field] = self.bot_sign

    async def game_over(self, playerone, playertwo):
        if (
            (
                self.field[0] == self.player_sign
                and self.field[1] == self.player_sign
                and self.field[2] == self.player_sign
            )
            or (
                self.field[0] == self.player_sign
                and self.field[3] == self.player_sign
                and self.field[6] == self.player_sign
            )
            or (
                self.field[2] == self.player_sign
                and self.field[5] == self.player_sign
                and self.field[8] == self.player_sign
            )
            or (
                self.field[6] == self.player_sign
                and self.field[7] == self.player_sign
                and self.field[8] == self.player_sign
            )
            or (
                self.field[0] == self.player_sign
                and self.field[4] == self.player_sign
                and self.field[8] == self.player_sign
            )
            or (
                self.field[2] == self.player_sign
                and self.field[4] == self.player_sign
                and self.field[6] == self.player_sign
            )
            or (
                self.field[1] == self.player_sign
                and self.field[4] == self.player_sign
                and self.field[7] == self.player_sign
            )
            or (
                self.field[3] == self.player_sign
                and self.field[4] == self.player_sign
                and self.field[5] == self.player_sign
            )
        ):
            await self.base.edit(
                embed=discord.Embed(color=0xFC80B2)
                .add_field(
                    name=f"**Tic Tac Toe: {playerone.name} vs {playertwo.name}**",
                    value=f'{"".join(self.field[0:3])}\n{"".join(self.field[3:6])}\n{"".join(self.field[6:9])}',
                )
                .set_footer(
                    text=f"The winner is {playerone.name}!",
                    icon_url=playerone.avatar_url,
                )
            )
            return True
        if (
            (
                self.field[0] == self.bot_sign
                and self.field[1] == self.bot_sign
                and self.field[2] == self.bot_sign
            )
            or (
                self.field[0] == self.bot_sign
                and self.field[3] == self.bot_sign
                and self.field[6] == self.bot_sign
            )
            or (
                self.field[2] == self.bot_sign
                and self.field[5] == self.bot_sign
                and self.field[8] == self.bot_sign
            )
            or (
                self.field[6] == self.bot_sign
                and self.field[7] == self.bot_sign
                and self.field[8] == self.bot_sign
            )
            or (
                self.field[0] == self.bot_sign
                and self.field[4] == self.bot_sign
                and self.field[8] == self.bot_sign
            )
            or (
                self.field[2] == self.bot_sign
                and self.field[4] == self.bot_sign
                and self.field[6] == self.bot_sign
            )
            or (
                self.field[1] == self.bot_sign
                and self.field[4] == self.bot_sign
                and self.field[7] == self.bot_sign
            )
            or (
                self.field[3] == self.bot_sign
                and self.field[4] == self.bot_sign
                and self.field[5] == self.bot_sign
            )
        ):
            await self.base.edit(
                embed=discord.Embed(color=0xFC80B2)
                .add_field(
                    name=f"**Tic Tac Toe: {playerone.name} vs {playertwo.name}**",
                    value=f'{"".join(self.field[0:3])}\n{"".join(self.field[3:6])}\n{"".join(self.field[6:9])}',
                )
                .set_footer(
                    text=f"The winner is {playertwo.name}!",
                    icon_url=playertwo.avatar_url,
                )
            )
            return True
        elif not any([f == self.blank for f in self.field]):
            await self.base.edit(
                embed=discord.Embed(color=0xFC80B2)
                .add_field(
                    name=f"**Tic Tac Toe: {playerone.name} vs {playertwo.name}**",
                    value=f'{"".join(self.field[0:3])}\n{"".join(self.field[3:6])}\n{"".join(self.field[6:9])}',
                )
                .set_footer(text=f"It's a tie!", icon_url=self.ctx.guild.icon_url)
            )
            return True
        return False

    async def update(self, playerone, playertwo):
        await self.base.edit(
            embed=discord.Embed(color=0xFC80B2)
            .add_field(
                name=f"**Tic Tac Toe: {playerone.name} vs {playertwo.name}**",
                value=f'{"".join(self.field[0:3])}\n{"".join(self.field[3:6])}\n{"".join(self.field[6:9])}',
            )
            .set_footer(
                text=f"{self.ctx.bot.get_user(self.whoturns[self.ctx.channel.id]).name}'s turn now",
                icon_url=self.ctx.bot.get_user(
                    self.whoturns[self.ctx.channel.id]
                ).avatar_url,
            )
        )

    async def regather_turn(self, playerone, playertwo):
        if self.whoturns[self.ctx.channel.id] == playerone.id:
            self.whoturns[self.ctx.channel.id] = playertwo.id
        else:
            self.whoturns[self.ctx.channel.id] = playerone.id

    async def _remove_reaction(self, react, user):
        try:
            await self.base.remove_reaction(react, user)
        except BaseException:
            pass

    def get_rand_move(self):
        try:
            self.field[
                random.choice([f for f in range(9) if self.field[f] == self.blank])
            ] = self.bot_sign
        except BaseException:
            pass

    async def main(self, playerone=None, playertwo=None):

        playerone = self.ctx.author

        if playertwo is None:
            playertwo = self.ctx.me

        self.whoturns[self.ctx.channel.id] = random.choice(
            (playerone, playertwo)).id
        self.base = await self.ctx.send(
            embed=discord.Embed(color=0xFC80B2)
            .add_field(
                name=f"**Tic Tac Toe: {playerone.name} vs {playertwo.name}**",
                value=f'{"".join(self.field[0:3])}\n{"".join(self.field[3:6])}\n{"".join(self.field[6:9])}',
            )
            .set_footer(
                text=f"{self.ctx.bot.get_user(self.whoturns[self.ctx.channel.id]).name}'s turn now",
                icon_url=self.ctx.bot.get_user(
                    self.whoturns[self.ctx.channel.id]
                ).avatar_url,
            )
        )

        for react in self.buttons:
            await self.base.add_reaction(str(react))

        def check(r, u):
            if u.id != self.whoturns[self.ctx.channel.id]:
                return False
            elif str(r) not in self.buttons.keys():
                return False
            elif r.message.id != self.base.id:
                return False
            elif u.id in self.ctx.bot.blacklist:
                return False
            elif u.bot:
                return False
            return True

        while True:

            await self.update(playerone, playertwo)

            if (
                playertwo == self.ctx.me
                and self.whoturns[self.ctx.channel.id] == self.ctx.me.id
            ):
                self.get_rand_move()
                if await self.game_over(playerone, playertwo):
                    break

            else:
                try:
                    react, user = await self.ctx.bot.wait_for(
                        "reaction_add", check=check, timeout=60
                    )
                except asyncio.TimeoutError:
                    await self.base.edit(
                        embed=discord.Embed(color=0xFC80B2)
                        .add_field(
                            name=f"**Tic Tac Toe: {playerone.name} vs {playertwo.name}**",
                            value=f'{"".join(self.field[0:3])}\n{"".join(self.field[3:6])}\n{"".join(self.field[6:9])}',
                        )
                        .set_footer(
                            text=f"Timed out!",
                            icon_url="https://i.imgur.com/UvjHUSp.png",
                        )
                    )
                control = self.buttons.get(str(react))
                if control == "stop":
                    return await self.base.edit(
                        embed=discord.Embed(color=0xFC80B2)
                        .add_field(
                            name=f"**Tic Tac Toe: {playerone.name} vs {playertwo.name}**",
                            value=f'{"".join(self.field[0:3])}\n{"".join(self.field[3:6])}\n{"".join(self.field[6:9])}',
                        )
                        .set_footer(
                            text=f"{user.name} stopped the game!",
                            icon_url=user.avatar_url,
                        )
                    )
                field = int(control) - 1
                if self.field[field] != self.blank:
                    continue

                self.make_move(field, playerone)
                if await self.game_over(playerone, playertwo):
                    break
                await self._remove_reaction(react, user)

            await self.update(playerone, playertwo)
            await self.regather_turn(playerone, playertwo)


class Games(commands.Cog):
    """Play with me~"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/22XCUqu.png"
        self.selecting = {}
        self.games = {}
        self._controls = {"🎮": "play", "⛔": "cancel"}

        self.buttons = {"1\u20e3": "1", "2\u20e3": "2", "⏹": "stop"}

    async def game_selector(self, ctx, game: str, gameclass, game_url: str):
        def check(r, u):
            if u != ctx.author:
                return False
            elif str(r) not in self.buttons.keys():
                return False
            elif r.message.id != self.base.id:
                return False
            elif u.id in self.bot.blacklist:
                return False
            elif u.bot:
                return False
            return True

        def _reaction_check(r, u):
            if not str(r) in self._controls:
                return False
            elif u == ctx.me:
                return False
            elif u != ctx.author and str(r) == "⛔":
                return False
            elif u == ctx.author and str(r) == "🎮":
                return False
            elif u.id in self.bot.blacklist:
                return False
            return True

        if self.games.get(
                ctx.channel.id) or self.selecting.get(
                ctx.channel.id):
            return await ctx.send(
                ":warning: | **Other game is already running here. Try another channel**",
                delete_after=5,
            )

        self.selecting[ctx.channel.id] = True
        self.base = await ctx.send(
            embed=discord.Embed(
                color=random.randint(0x000000, 0xFFFFFF),
                timestamp=ctx.message.created_at,
            )
            .add_field(
                name=f"**{game}**",
                value="**:fire: Select mode to play:**\n1\u20e3`: solo`\n2\u20e3`: multi`",
            )
            .set_footer(text=f"Mode Selection Menu", icon_url=ctx.author.avatar_url)
        )
        for react in self.buttons:
            try:
                await self.base.add_reaction(str(react))
            except BaseException:
                pass

        try:
            while self.selecting[ctx.channel.id]:
                try:
                    react, user = await self.bot.wait_for(
                        "reaction_add", check=check, timeout=60
                    )
                except asyncio.TimeoutError:
                    await self.base.delete()
                    await ctx.send(":clock2: | **Timed out!**", delete_after=5)
                    del self.selecting[ctx.channel.id]
                    return
                control = self.buttons.get(str(react))
                if control == "1":
                    try:
                        await self.base.delete()
                        del self.selecting[ctx.channel.id]
                    except BaseException:
                        continue

                    game = gameclass(ctx)
                    self.games[ctx.channel.id] = game
                    await game.main()
                    del self.games[ctx.channel.id]

                elif control == "2":
                    try:
                        await self.base.delete()
                    except BaseException:
                        continue

                    try:
                        inv = await ctx.send(
                            embed=discord.Embed(
                                color=random.randint(0x000000, 0xFFFFFF),
                                timestamp=ctx.message.created_at,
                            )
                            .add_field(
                                name=f"**{ctx.author.name} seeks for a {game} game!**",
                                value=f"React with 🎮 to play!\n{ctx.author.mention}, if you want to cancel the game, react with ⛔\n\n🎚 This will automatically expire in 30 seconds",
                            )
                            .set_footer(
                                text=ctx.author.name, icon_url=ctx.author.avatar_url
                            )
                            .set_thumbnail(url=game_url)
                        )
                        for react in self._controls:
                            try:
                                await inv.add_reaction(str(react))
                            except BaseException:
                                pass
                        reaction, user = await self.bot.wait_for(
                            "reaction_add", check=_reaction_check, timeout=30
                        )
                        control = self._controls.get(str(reaction))

                        if control == "play":
                            try:
                                await inv.delete()
                                del self.selecting[ctx.channel.id]
                            except BaseException:
                                continue

                            game = gameclass(ctx)
                            self.games[ctx.channel.id] = game
                            await game.main(ctx.author, user)
                            del self.games[ctx.channel.id]

                        elif control == "cancel":
                            try:
                                await inv.delete()
                                del self.selecting[ctx.channel.id]
                            except BaseException:
                                continue

                            await ctx.send(
                                ":information_source: | **You have cancelled your game request**",
                                delete_after=5,
                            )

                    except BaseException:
                        await inv.delete()
                        await ctx.send(
                            f":clock2: | **Timed out. No one wanted to join your game, {ctx.author.mention} :cry:**",
                            delete_after=30,
                        )
                        try:
                            del self.selecting[ctx.channel.id]
                        except BaseException:
                            pass

                elif control == "stop":
                    try:
                        await ctx.send(
                            ":information_source: | **You have cancelled game selection**",
                            delete_after=5,
                        )
                        await self.base.delete()
                        del self.selecting[ctx.channel.id]
                    except BaseException:
                        pass

        except KeyError:
            pass

    @commands.command(aliases=["ttt"])
    @commands.guild_only()
    async def tictactoe(self, ctx):
        """Play Tic Tac Toe with me!"""
        await self.game_selector(
            ctx, "Tic Tac Toe", TicTacToe, "https://i.imgur.com/kUSELAG.png"
        )


def setup(bot):
    bot.add_cog(Games(bot))
