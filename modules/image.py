import discord
from textwrap import fill
from discord.ext import commands
import aiohttp
from PIL import Image, ImageDraw, ImageFont
from functools import partial
from io import BytesIO
from typing import Union
from discord.ext.commands.cooldowns import BucketType


class ImageModule:
    """Playing with images is awesome!~"""

    def __init__(self, bot):
        self.bot = bot
        
        self._font_path = f"{self.bot.path}/fonts/Azoft-Sans.ttf"
        self.thumbnail = "https://i.imgur.com/mb1sg1b.png"

    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:
        async with self.bot.session.get(user.avatar_url_as(format="png")) as response:
            return await response.read()

    async def get_picture(self, picture_url: str) -> bytes:
        async with self.bot.session.get(picture_url) as response:
            return await response.read()

    @staticmethod
    def processing(avatar_bytes: bytes, colour: tuple) -> BytesIO:
        with Image.open(BytesIO(avatar_bytes)) as im:
            with Image.new("RGB", im.size, colour) as background:
                rgb_avatar = im.convert("RGB")
                with Image.new("L", im.size, 0) as mask:
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.ellipse([(0, 0), im.size], fill=255)
                    background.paste(rgb_avatar, (0, 0), mask=mask)
                final_buffer = BytesIO()
                background.save(final_buffer, "png")
        final_buffer.seek(0)

        return final_buffer

    @staticmethod
    def do_filter(avatar_bytes: bytes, color):
        with Image.open(BytesIO(avatar_bytes)) as image:
            mask = image.convert("L").point(lambda x: 0 if x < 32 else x, "L")
            with Image.new("RGBA", image.size, color) as new_image:
                new_image.paste(image, (0, 0), mask)
                bytes_io = BytesIO()
                new_image.save(bytes_io, "png")
                bytes_io.seek(0)
        return bytes_io

    @staticmethod
    def do_drake_meme(drake_bytes: bytes, no: str, yes: str, path):
        with Image.open(BytesIO(drake_bytes)) as image:
            draw = ImageDraw.Draw(image)
            draw.text(
                (250, 20),
                fill(no if len(no) < 50 else no[:50], 17),
                (0, 0, 0),
                font=ImageFont.truetype(path, 40),
            )
            draw.text(
                (250, 250),
                fill(yes if len(yes) < 50 else yes[:50], 17),
                (0, 0, 0),
                font=ImageFont.truetype(path, 40),
            )
            bytes_io = BytesIO()
            image.save(bytes_io, "png")
            bytes_io.seek(0)
        return bytes_io

    @commands.command()
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def circle(self, ctx, *, member: discord.Member = None):
        """Display the user's avatar on their colour"""
        member = member or ctx.author

        async with ctx.typing():
            if isinstance(member, discord.Member):
                member_colour = member.colour.to_rgb()
            else:
                member_colour = (0, 0, 0)

            avatar_bytes = await self.get_avatar(member)

            final_buffer = await self.bot.loop.run_in_executor(
                None, partial(self.processing, avatar_bytes, member_colour)
            )

            await ctx.send(
                content=f"<:Ok:501773759011749898> | **Generated for {ctx.author.mention}**",
                file=discord.File(filename=f"{member.name}.png", fp=final_buffer),
            )

    @commands.command()
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def filter(
        self, ctx, color: commands.clean_content, *, member: discord.Member = None
    ):
        """Filter an avatar
        For example, @Naoko filter #170041 F4stZ4p
        """
        member = member or ctx.author

        try:
            async with ctx.typing():
                avatar_bytes = await self.get_avatar(member)
                final_buffer = await self.bot.loop.run_in_executor(
                    None, partial(self.do_filter, avatar_bytes, color)
                )
                await ctx.send(
                    content=f"<:Ok:501773759011749898> | **Generated for {ctx.author.mention}**",
                    file=discord.File(filename=f"{member.name}.png", fp=final_buffer),
                )
        except:
            await ctx.send(
                f"<:Error:501773759217401856> | **Please, check the color (`{color}` is not correct, for example `#170041` is correct)**",
                delete_after=15,
            )

    @commands.command()
    @commands.cooldown(1.0, 10.0, commands.BucketType.user)
    async def drake(self, ctx, no, *, yes):
        """
        Generates a Drake meme
        For example, n.drake "Using Naoko" Using MEE6
        """
        async with ctx.typing():
            drake_bytes = await self.get_picture("https://i.imgur.com/aaiqFBu.png")
            final_buffer = await self.bot.loop.run_in_executor(
                None,
                partial(
                    self.do_drake_meme,
                    drake_bytes,
                    no,
                    yes,
                    self._font_path,
                ),
            )
            await ctx.send(
                content=f"<:Ok:501773759011749898> | **Generated for {ctx.author.mention}**",
                file=discord.File(filename=f"Drake.png", fp=final_buffer),
            )


def setup(bot):
    bot.add_cog(ImageModule(bot))
