import discord
import random
from checks.naoko_checks import *
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class NSFW():
    """NSFW Commands 🔞"""
    def __init__(self, bot):
        self.bot = bot
        self.thumbnail = "https://i.imgur.com/ivmKTvu.png"
        self.tags = ('feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk', 'ngif', 'meow', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom', 'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'Random_hentai_gif', 'smallboobs', 'hug', 'ero')
    
    @nsfw()
    @commands.command(name="neko", aliases=['catgirl'])
    @commands.cooldown(1.0, 5.0, commands.BucketType.user)
    async def _neko(self, ctx, *, tag: str = None):
        """Gives you random neko picture. Channel must be NSFW to use this command. Leave the tag field empty to randomize neko.
            ---
            Tags are: feet, yuri, trap, futanari, hololewd, lewdkemo, solog, feetg, 
            cum, erokemo, les, wallpaper, lewdk, ngif, meow, tickle, lewd, feed, gecg,
            eroyuri, eron, cum_jpg, bj, nsfw_neko_gif, solo, kemonomimi, nsfw_avatar,
            gasm, poke, anal, slap, hentai, avatar, erofeet, holo, keta, blowjob, pussy,
            tits, holoero, lizard, pussy_jpg, pwankg, classic, kuni, waifu, pat, 8ball, kiss,
            femdom, neko, spank, cuddle, erok, fox_girl, boobs, Random_hentai_gif, smallboobs,
            hug, ero
        """
        try:
            if tag is None: tag = random.choice(self.tags)
            tag = tag.lower()
            if tag == "random_hentai_gif": tag = tag.capitalize()
            async with self.bot.session.get(f'https://nekos.life/api/v2/img/{tag}') as resp:
                data = await resp.json()
                embedneko = discord.Embed(color=random.randint(0x000000, 0xFFFFFF), title=f"Neko :3 - {tag}", timestamp=ctx.message.created_at)
                embedneko.set_image(url=f'{data.get("url")}')
                embedneko.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embedneko)
        except:
            embedneko = discord.Embed(color=random.randint(0x000000, 0xFFFFFF), timestamp=ctx.message.created_at)
            embedneko.set_footer(text=f"{ctx.author.name}, an error occured. API trouble or no tags found for {tag}.", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embedneko)


def setup(bot):
    bot.add_cog(NSFW(bot))