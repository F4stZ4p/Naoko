from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import re
from platform import python_version
import gc
import copy
import os, sys

# to expose to the eval command
import datetime
from collections import Counter
from utils.naoko_shell import shell
from checks.naoko_checks import *
from utils.naoko_updater import _update

class Admin:

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @owner()  
    @commands.command(pass_context=True, hidden=True, name='eval', aliases=['evaluate'])
    async def _eval(self, ctx, *, body: str):
        env = {
            'self': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        await ctx.message.add_reaction('a:loading:451342728077508608')
        
        try:
            exec(to_compile, env)
        except Exception as e:
            await ctx.message.remove_reaction('a:loading:451342728077508608', member=ctx.me)
            await ctx.message.add_reaction('naokoerror:447495055603662849')
            fooem = discord.Embed(color=0xff0000)
            fooem.add_field(name="Code evaluation was not successful.", value=f'```\n{e.__class__.__name__}: {e}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
            fooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
            fooem.timestamp = ctx.message.created_at
            return await ctx.send(embed=fooem)

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.message.remove_reaction('a:loading:451342728077508608', member=ctx.me)
            await ctx.message.add_reaction('naokoerror:447495055603662849')
            fooem = discord.Embed(color=0xff0000)
            fooem.add_field(name="Code evaluation was not successful.", value=f'```py\n{value}{traceback.format_exc()}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
            fooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
            fooem.timestamp = ctx.message.created_at
            await ctx.send(embed=fooem)
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.remove_reaction('a:loading:451342728077508608', member=ctx.me)
                await ctx.message.add_reaction('naokotick:447494238872141827')
            except:
                pass

            if ret is None:
                if value:
                    sfooem = discord.Embed(color=0x170041)
                    sfooem.add_field(name="Code evaluation was successful!", value=f'```py\n{value}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                    sfooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
                    sfooem.timestamp = ctx.message.created_at
                    await ctx.send(embed=sfooem)
            else:
                self._last_result = ret
                ssfooem = discord.Embed(color=0x170041)
                ssfooem.add_field(name="Code evaluation was successful!", value=f'```py\n{value}{ret}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                ssfooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
                ssfooem.timestamp = ctx.message.created_at
                await ctx.send(embed=ssfooem)

    @owner() 
    @commands.command(hidden=True, aliases=['die'])
    async def logout(self, ctx):
        embed = discord.Embed(color=1507393)
        embed.add_field(name='Naoko logout', value="I've successfully logged out from Discord.")
        embed.set_footer(
            text='Command requested by {}'.format(ctx.author),
            icon_url='https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/key.ico')
        await ctx.channel.send(embed=embed)
        await self.bot.logout()
           
    @owner() 
    @commands.command(hidden=True, aliases=["say","print"])
    async def echo(self, ctx, *, content):
        await ctx.send(content)

    @owner() 
    @commands.command(pass_context=True, aliases=["st"], hidden=True)
    async def sendtyping(self, ctx):
        await ctx.message.add_reaction('a:loading:451342728077508608')
        await ctx.trigger_typing()
        await asyncio.sleep(10)
        await ctx.message.remove_reaction('a:loading:451342728077508608', member=ctx.me)
        await ctx.message.add_reaction('naokotick:447494238872141827')
        
    @owner() 
    @commands.command(pass_context=True, hidden=True)
    async def speedup(self, ctx):
        await ctx.message.add_reaction('a:loading:451342728077508608')
        gc.collect()
        del gc.garbage[:]
        await ctx.message.remove_reaction('a:loading:451342728077508608', member=ctx.me)
        await ctx.message.add_reaction('naokotick:447494238872141827')
        
    @owner() 
    @commands.group(invoke_without_command=True, hidden=True)
    async def blacklist(self, ctx):
        await ctx.author.send('**BADD** / **BREMOVE** / **BDISCARD** / **BSHOW**')
        
    @owner() 
    @blacklist.command(hidden=True)
    async def badd(self, ctx, user: discord.User, *, reason: str):
        self.bot.blacklist.append(user.id)
        try:
            await user.send(f'**{user.mention}**, **{ctx.author}** blocked you from using the bot for: **{reason}**')
        except:
            await ctx.send(':warning: | **Unable to send DMs to specified user.**')
        await ctx.send(':ok_hand:')
        
    @owner() 
    @blacklist.command(hidden=True)
    async def bremove(self, ctx, *, user: discord.User):
        self.bot.blacklist.remove(user.id)
        try:
            await user.send(f'**{user.mention}**, **{ctx.author}** unblocked you from using the bot. Don\'t abuse the bot again or you will get blocked **permanently**.')
        except:
            await ctx.send(':warning: | **Unable to send DMs to specified user.**')
        await ctx.send(':ok_hand:')
        
    @owner() 
    @blacklist.command(hidden=True)
    async def bdiscard(self, ctx):
        self.bot.blacklist = []
        await ctx.send(':ok_hand:')

    @owner() 
    @blacklist.command(hidden=True)
    async def bshow(self, ctx):
        await ctx.send(f'``{self.bot.blacklist}``')

    @owner() 
    @commands.group(invoke_without_command=True, hidden=True)
    async def whitelist(self, ctx):
        await ctx.author.send('**WADD** / **WREMOVE** / **WDISCARD** / **WSHOW**')
        
    @owner() 
    @whitelist.command(hidden=True)
    async def wadd(self, ctx, *, user: discord.User):
        self.bot.whitelist.append(user.id)
        await ctx.send(':ok_hand:')
       
    @owner()  
    @whitelist.command(hidden=True)
    async def wremove(self, ctx, *, user: discord.User):
        self.bot.whitelist.remove(user.id)
        await ctx.send(':ok_hand:')
        
    @owner() 
    @whitelist.command(hidden=True)
    async def wdiscard(self, ctx):
        self.bot.whitelist = [340745895932854272]
        await ctx.send(':ok_hand:')

    @owner() 
    @whitelist.command(hidden=True)
    async def wshow(self, ctx):
        await ctx.send(f'``{self.bot.whitelist}``')

    @owner() 
    @commands.command(hidden=True, aliases=["impersonate"])
    async def runas(self, ctx, member: discord.Member, *, cmd):
        msg = copy.copy(ctx.message)
        msg.content = f"{ctx.me.mention} {cmd}"
        msg.author = member
        await self.bot.process_commands(msg)

    @owner() 
    @commands.command(hidden=True, aliases=['r'])
    async def restart(self, ctx):
        """Restarts the bot"""
        await ctx.send(embed=discord.Embed(color=0x1D99F3).set_footer(text="Restarting...", icon_url="https://i.imgur.com/mXZbOEz.png"))
        os.execl(sys.executable, sys.executable, * sys.argv)

    @owner() 
    @commands.command(hidden=True)
    async def cleanup(self, ctx):
        await ctx.channel.purge(limit=30, check=lambda m: m.author.id == ctx.me.id)
        await ctx.send(':ok_hand:', delete_after=5)

    @owner() 
    @commands.command(hidden=True)
    async def combo(self, ctx, *, commands: str):
        for command in commands.split(' && '):
            await ctx.invoke(self.bot.get_command(command))
        await ctx.message.add_reaction(':Ok:501773759011749898')

    @owner() 
    @commands.group(hidden=True, invoke_without_command=True)
    async def shell(self, ctx):
        await ctx.author.send(f'{ctx.prefix}shell hastebin / textfile / default ``<Your Query>``')

    @owner() 
    @shell.command(hidden=True)
    async def default(self, ctx, *, shellcommand):
        emb = await ctx.send(embed=discord.Embed(color=0x67d655).set_footer(text="Running...", icon_url="https://i.imgur.com/el2Wofz.gif"))
        b = await self.bot.loop.run_in_executor(None, shell, shellcommand)
        if b == "": b = "ℹ | No output"
        try:
            await emb.edit(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**Done**", value=f"```BAT\n{b}```").set_footer(text="Action done at:", icon_url=ctx.me.avatar_url))
        except:
            try:
                async with self.bot.session.post("https://hastebin.com/documents", data=b) as post:
                    post = await post.json()
                    await emb.edit(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**Done. Output too long, uploaded to hastebin**", value=f"**[Click](https://hastebin.com/{post['key']})**").set_footer(text="Action done at:", icon_url=ctx.me.avatar_url))
            except:
                await emb.edit(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**Done. Output too long, uploaded to hastebin**", value=f"**Uploading to hastebin failed. Sorry.**").set_footer(text="Action done at:", icon_url=ctx.me.avatar_url))
        del b

    @owner() 
    @shell.command(hidden=True)
    async def hastebin(self, ctx, *, shellcommand):
        emb = await ctx.send(embed=discord.Embed(color=0x67d655).set_footer(text="Running...", icon_url="https://i.imgur.com/el2Wofz.gif"))
        b = await self.bot.loop.run_in_executor(None, shell, shellcommand)
        if b == "": b = "ℹ | No output"
        try:
            async with self.bot.session.post("https://hastebin.com/documents", data=b) as post:
                post = await post.json()
                await emb.edit(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**Done**", value=f"**[Click](https://hastebin.com/{post['key']})**").set_footer(text="Action done at:", icon_url=ctx.me.avatar_url))
        except:
            await ctx.send(':warning | **Uploading failed. Try textfile or default.**')
        del b

    @owner() 
    @shell.command(hidden=True)
    async def textfile(self, ctx, *, shellcommand):
        emb = await ctx.send(embed=discord.Embed(color=0x67d655).set_footer(text="Running...", icon_url="https://i.imgur.com/el2Wofz.gif"))
        b = await self.bot.loop.run_in_executor(None, shell, shellcommand)
        if b == "": b = "ℹ | No output"
        try:
            b = io.BytesIO(b.encode('utf-8'))
            try:
                await emb.delete()
            except:
                pass
            await ctx.send(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**Done**", value="Output redirected to Text File.").set_footer(text="Action done at:", icon_url=ctx.me.avatar_url), file=discord.File(b, filename='Shell.txt'))
        except Exception as e:
            await emb.edit(content=f':warning: | **Failed: {e}. Try default.**')
        del b
        del baa

    @owner() 
    @commands.command(hidden=True)
    async def sql(self, ctx, *, query):
        try:
            emb = await ctx.send(embed=discord.Embed(color=0x67d655).set_footer(text="Executing SQL Query...", icon_url="https://i.imgur.com/el2Wofz.gif"))
            await self.bot.db.execute(query)
            await emb.edit(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**SQL Query Executed Successfully!**", value=chr(173)).set_footer(text="Action done at:", icon_url=ctx.me.avatar_url))
        except Exception as e:
            await emb.edit(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**SQL Query Execution Failed!**", value=f"```css\n[Error: {e}]```").set_footer(text="Action done at:", icon_url=ctx.me.avatar_url))

    @commands.command(hidden=True)
    @owner()
    async def load(self, ctx, extension_name: str):
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            embed = discord.Embed(color=1507393)
            embed.set_footer(
                text='\n{}: {}\n'.format(type(e).__name__, str(e)),
                icon_url='https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/error.ico')
            await ctx.send(embed=embed, delete_after=10)
            return
        embed = discord.Embed(color=1507393)
        embed.set_footer(
            text='{} module loaded.'.format(extension_name),
            icon_url='https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/cogs.ico')
        await ctx.send(embed=embed, delete_after=10)

    @commands.command(hidden=True)
    @owner()
    async def unload(self, ctx, extension_name: str):
        self.bot.unload_extension(extension_name)
        embed = discord.Embed(color=1507393)
        embed.set_footer(
            text='{} module unloaded.'.format(extension_name),
            icon_url='https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/cogs.ico')
        await ctx.send(embed=embed, delete_after=10)
    
    @commands.command(hidden=True)
    @owner()
    async def reload(self, ctx, *, module):
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
            embed = discord.Embed(color=1507393)
            embed.set_footer(text='Reloaded {} module.'.format(module), icon_url='https://raw.githubusercontent.com/F4stZ4p/resources-for-discord-bot/master/cogs.ico')
            await ctx.send(embed=embed, delete_after=10)
        except Exception as e:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```', delete_after=10)

    @commands.command(hidden=True)
    @owner()
    async def update(self, ctx):
        """Update the bot and reload all modules"""
        emb = await ctx.send(embed=discord.Embed(color=0x67d655).set_footer(text="Updating...", icon_url="https://i.imgur.com/el2Wofz.gif"))
        b = await self.bot.loop.run_in_executor(None, _update, os.path.dirname(os.path.realpath(__file__)))
        await emb.edit(embed=discord.Embed(color=0x67d655, timestamp=ctx.message.created_at).add_field(name="**Updated**", value=f"```fix\n{b}```").set_footer(text="Updated at:", icon_url=ctx.me.avatar_url))
        self.bot.stat = await self.bot.loop.run_in_executor(None, shell, 'git show -n 1 -s --format="[%h] %s"')
        del b

        for extension in self.bot.startup_extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e:
                await ctx.send(f'```python\n{e}\n```')
        await ctx.send(':information_source: | **Tried to reload all modules**')

def setup(bot):
    bot.add_cog(Admin(bot))