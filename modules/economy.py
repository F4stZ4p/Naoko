import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from checks.naoko_checks import *
import asyncpg
import random
import asyncio


class Economy:
    """Economy commands"""

    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/KnwF1Gc.png"
        self.createq = "INSERT INTO users (money, id) VALUES ($1, $2)"
        self.gtrq = "UPDATE users SET MONEY = $1 WHERE ID = $2"
        self._jobs = (
            "Aerospace Engineer",
            "Nurse",
            "Doctor",
            "Killer",
            "Tax Collector",
            "Farmer",
            "Teacher",
            "Animal Scientist",
            "Film Producer",
            "Programmer",
        )

    async def _credit_card_generator(self, context, targetbalance, target):
        try:
            await context.send(
                embed=discord.Embed(
                    color=0x191970, timestamp=context.message.created_at
                )
                .add_field(
                    name=f"**:credit_card: {target.name}'s Credit Card**",
                    value=f"**Credits count: ``{targetbalance}`` <a:bitcoin:506081804567052288>**",
                )
                .set_footer(
                    text=f"Credit card generated at:",
                    icon_url=context.author.avatar_url,
                )
                .set_thumbnail(url=target.avatar_url)
            )
        except:
            pass

    @commands.command(aliases=["bal", "credits"])
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def balance(self, ctx, target: discord.User = None):
        """Show your balance"""
        if target is None:
            target = ctx.author
        async with self.bot.db.acquire() as con:
            a = await con.fetchval(f"SELECT MONEY FROM users WHERE ID = {target.id};")
            if a is not None:
                await self._credit_card_generator(ctx, a, target)
            else:
                await ctx.send(
                    f":warning: | **{target} does not have an Economy Account. Create one with @Naoko create**",
                    delete_after=15,
                )
            await self.bot.db.release(con)
            
    @commands.command(aliases=["vb", "bonus"])
    @commands.cooldown(1.0, 20.0, commands.BucketType.user)
    async def votebonus(self, ctx):
        """Claim your bonus for voting"""
        async with self.bot.session.get(
            f"https://discordbots.org/api/bots/{ctx.me.id}/check?userId={ctx.author.id}",
            
            headers={
                "Authorization": self.bot.config.dbltoken
            }

        ) as voted:
            
            voted = await resp.json()
            
            if voted == 0:
                return await ctx.send(
                    ":x: **Sorry, you didn't vote for me**",
                    delete_after=5
                )
            
            bonus = random.randint(
                1000, 3000
            )
            
            async with self.bot.db.acquire() as con:
                await con.execute(
                    f"UPDATE users SET money = money + {bonus} WHERE id = {ctx.author.id}"
                )
                
                await self.bot.db.release(con)
                
            await ctx.send(
                f":package: | **You successfully claimed your `{bonus}` vote bonus! Thanks for voting!**",
                delete_after=5
            )
            
            
            
    @commands.command(aliases=["lb", "leaders"])
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def leaderboard(self, ctx):
        """Shows global leaderboard"""
        async with self.bot.db.acquire() as con:
            
            a = await con.fetch(
                "SELECT * FROM users ORDER BY money DESC LIMIT 3"
            )
            
            await self.bot.db.release(con)
            
            await ctx.send(
                embed=discord.Embed(
                    title="The Richest People", 
                    color=random.randint(0x000000, 0xFFFFFF),
                    timestamp=ctx.message.created_at
                )
                .add_field(
                    name="**:dizzy: Leaders**", 
                    value=
f"""
:first_place: | {self.bot.get_user(a[0][0]).mention}: **{a[0][1]}** <a:bitcoin:506081804567052288>
:second_place: | {self.bot.get_user(a[1][0]).mention}: **{a[1][1]}** <a:bitcoin:506081804567052288>
:third_place: | {self.bot.get_user(a[2][0]).mention}: **{a[2][1]}** <a:bitcoin:506081804567052288>
"""
                )
                .set_footer(
                    text=f"These stats are global, {ctx.author.name}",
                    icon_url=ctx.author.avatar_url
                )
                .set_thumbnail(
                    url=self.thumbnail
                )
            )
    
    @commands.command()
    @commands.cooldown(1.0, 3600.0, commands.BucketType.user)
    async def create(self, ctx):
        """Create your character"""
        async with self.bot.db.acquire() as con:
            a = await con.fetchval(f"SELECT * FROM users WHERE ID = {ctx.author.id};")
            if a is not None:
                await ctx.send(
                    ":warning: | **You already have Economy Account.**", delete_after=15
                )

            else:
                await con.execute(self.createq, 0, ctx.author.id)
                await ctx.send(
                    ":information_source: | **Successfully created your character. Do @Naoko balance to view your balance and @Naoko work to earn money**",
                    delete_after=15,
                )
        await self.bot.db.release(con)

    @account()
    @commands.command()
    @commands.cooldown(1.0, 3600.0, commands.BucketType.user)
    async def delete_account(self, ctx):
        """Delete your economy account"""
        async with self.bot.db.acquire() as con:
            await con.execute(f"DELETE FROM users WHERE ID = {ctx.author.id};")
            await con.execute(f"DELETE FROM cars WHERE ID = {ctx.author.id};")
        await self.bot.db.release(con)
        await ctx.send(
            ":information_source: | **Successfully deleted your character :(**",
            delete_after=15,
        )

    @account()
    @commands.command()
    @commands.cooldown(1.0, 30.0, commands.BucketType.user)
    async def work(self, ctx):
        """Work and earn some $$$"""
        async with self.bot.db.acquire() as con:
            rmoney = random.randint(0, 350)
            a = await con.fetchval(
                f"SELECT MONEY FROM users WHERE ID = {ctx.author.id};"
            )
            e = await ctx.send(
                f"{ctx.author.mention} is working hard as {random.choice(self._jobs)}..."
            )
            await asyncio.sleep(10)
            await con.execute(self.gtrq, a + rmoney, ctx.author.id)
            await e.edit(
                content=f"{ctx.author.mention} worked hard and earned **{rmoney}** <a:bitcoin:506081804567052288>"
            )
        await self.bot.db.release(con)

    @account()
    @commands.command()
    @commands.cooldown(1.0, 3.0, commands.BucketType.user)
    async def transfer(self, ctx, where: discord.User, *, money: int):
        """Transfer money to someone. Example: n.transfer F4stZ4p 5000"""
        if where.bot:
            await ctx.send(
                ":information_source: | **You can't transfer money to a bot**",
                delete_after=15,
            )
        elif where == ctx.author:
            await ctx.send(
                ":information_source: | **You can't transfer money to yourself**",
                delete_after=15,
            )
        else:
            async with self.bot.db.acquire() as con:
                a = await con.fetchval(
                    f"SELECT MONEY FROM users WHERE ID = {ctx.author.id};"
                )
                if a is not None and a < money:
                    await ctx.send(
                        f":warning: | **You do not have enough money (``{money}``/``{a}``). Earn some with @Naoko work**",
                        delete_after=15,
                    )
                elif money < 10:
                    await ctx.send(
                        f":warning: | **Minimal sum for transfer is 10 <a:bitcoin:506081804567052288>**",
                        delete_after=15,
                    )
                else:
                    a = await con.fetchval(
                        f"SELECT MONEY FROM users WHERE ID = {where.id};"
                    )
                    if a is None:
                        await ctx.send(
                            f":warning: | **{where} does not have an Economy Account. Suggest him/her create one with @Naoko create**",
                            delete_after=15,
                        )
                    else:
                        a = await con.fetchval(
                            f"SELECT MONEY FROM users WHERE ID = {ctx.author.id};"
                        )
                        b = await con.fetchval(
                            f"SELECT MONEY FROM users WHERE ID = {where.id};"
                        )
                        await con.execute(self.gtrq, a - money, ctx.author.id)
                        await con.execute(self.gtrq, b + money, where.id)
                        await ctx.send(
                            f":arrow_forward: | **Successfully sent ``{money}`` <a:bitcoin:506081804567052288> to {where}**",
                            delete_after=35,
                        )
                        try:
                            await where.send(
                                f":arrow_forward: | **Transfer Receipt from {ctx.author}: ``{money}`` <a:bitcoin:506081804567052288>**"
                            )
                        except:
                            pass
            await self.bot.db.release(con)

    @account()
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1.0, 3.0, commands.BucketType.user)
    async def car(self, ctx, u: discord.User = None):
        """Shows your car"""
        if u is None:
            u = ctx.author
        async with self.bot.db.acquire() as con:
            a = await con.fetchval(f"SELECT car FROM cars WHERE ID = {u.id};")
            if a is not None:
                await ctx.send(
                    embed=discord.Embed(color=random.randint(0x000000, 0xFFFFFF))
                    .add_field(name=f"**{u.name}'s Car**", value=chr(173))
                    .set_image(url=a)
                )
            else:
                await ctx.send(
                    f":information_source: | **{u.name} does not have a car yet. Buy one with `{ctx.prefix}car buy <car image url>`. It costs 10000 <a:bitcoin:506081804567052288>**",
                    delete_after=5,
                )
        await self.bot.db.release(con)

    @account()
    @car.command()
    @commands.cooldown(1.0, 3.0, commands.BucketType.user)
    async def buy(self, ctx, url: str = None):
        if url is None:
            await ctx.send(
                ":information_source: | **Please provide car image url!**",
                delete_after=5,
            )
        else:
            async with self.bot.db.acquire() as con:
                if (
                    await con.fetchval(
                        f"SELECT MONEY FROM users WHERE ID = {ctx.author.id}"
                    )
                ) < 10000:
                    await ctx.send(
                        ":information_source: | **You don't have enough money. You need 10000 <a:bitcoin:506081804567052288> to buy a car**",
                        delete_after=5,
                    )
                else:
                    a = await con.fetchval(
                        f"SELECT car FROM cars WHERE ID = {ctx.author.id};"
                    )
                    if a is None:
                        try:
                            await con.execute(
                                "INSERT INTO cars (ID, car) VALUES ($1, $2)",
                                ctx.author.id,
                                url,
                            )
                            await ctx.send(
                                f":information_source: | **You successfully bought car. Type `{ctx.prefix}car` to view it**",
                                delete_after=5,
                            )
                            a = await con.fetchval(
                                f"SELECT MONEY FROM users WHERE ID = {ctx.author.id};"
                            )
                            await con.execute(self.gtrq, a - 10000, ctx.author.id)
                        except Exception as e:
                            await ctx.send(
                                f":warning: | **An error occured: `{e}`. Looks like url is too long.**"
                            )

                    else:
                        try:
                            await con.execute(
                                "UPDATE cars SET car = $1 WHERE ID = $2",
                                url,
                                ctx.author.id,
                            )
                            await ctx.send(
                                f":information_source: | **Successfully updated your car. Type `{ctx.prefix}car` to view it**",
                                delete_after=5,
                            )
                            a = await con.fetchval(
                                f"SELECT MONEY FROM users WHERE ID = {ctx.author.id};"
                            )
                            await con.execute(self.gtrq, a - 10000, ctx.author.id)
                        except Exception as e:
                            await ctx.send(
                                f":warning: | **An error occured: `{e}`. Looks like url is too long.**"
                            )

            await self.bot.db.release(con)

    @account()
    @commands.command()
    @commands.cooldown(1.0, 3.0, commands.BucketType.user)
    async def flip(self, ctx, choice: str.lower, amount: int):
        """
        Gamble your money
        For example,
        @Naoko flip tails 200
        @Naoko flip heads 250
        """
        if (
            await self.bot.db.fetchval(
                f"SELECT MONEY FROM users WHERE id = {ctx.author.id}"
            )
        ) < amount:
            await ctx.send(
                "<:Error:501773759217401856> | **You don't have that much money, don't try cheating on me**",
                delete_after=5,
            )
        elif choice not in ("heads", "tails"):
            await ctx.send(
                "<:Error:501773759217401856> | **Only heads or tails are accepted, nothing else**",
                delete_after=5,
            )
        elif amount <= 0:
            await ctx.send(
                "<:Error:501773759217401856> | **Why are you betting no money? I see no point**",
                delete_after=5,
            )
        elif amount > 10000:
            await ctx.send(
                f"<:Error:501773759217401856> | **Find a better way to spend them, for example buy a car**",
                delete_after=5,
            )
        else:
            if random.choice(("heads", "tails")) == choice:
                async with self.bot.db.acquire() as con:
                    money = await con.fetchval(
                        f"SELECT MONEY FROM users WHERE id = {ctx.author.id}"
                    )
                    await con.execute(self.gtrq, money + amount, ctx.author.id)
                await self.bot.db.release(con)
                await ctx.send(
                    f"Awesome! You won **{amount}** <a:bitcoin:506081804567052288>!"
                )

            else:
                async with self.bot.db.acquire() as con:
                    money = await con.fetchval(
                        f"SELECT MONEY FROM users WHERE id = {ctx.author.id}"
                    )
                    await con.execute(self.gtrq, money - amount, ctx.author.id)
                await self.bot.db.release(con)
                await ctx.send(
                    f"Oh no! You lost **{amount}** <a:bitcoin:506081804567052288>!"
                )


def setup(bot):
    bot.add_cog(Economy(bot))
