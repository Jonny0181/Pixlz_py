import discord
import os
import asyncio
import datetime
import time
from datetime import timedelta
from utils import checks
from discord.ext import commands

wrap = "```py\n{}```"

class Dev:
    def __init__(self, pixlz):
        self.pixlz = pixlz
        print('Addon "{}" loaded.'.format(self.__class__.__name__))

    @commands.command()
    @commands.check(checks.is_owner)
    async def bavatar(self, ctx, url):
        """Changes Brooklyn's avatar."""
        with aiohttp.ClientSession() as s:
            async with s.get(url) as resp:
                await ctx.bot.user.edit(avatar=await resp.read())

    @commands.command(pass_context=True)
    @commands.check(checks.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            ctx.bot.unload_extension("modules.{}".format(name))
            ctx.bot.load_extension("modules.{}".format(name))
        except Exception as e:
            await ctx.send(e)
            return
        e = "Reloaded extention {}.py :ok_hand:".format(name)
        await ctx.send(e)

    @commands.command(pass_context=True)
    @commands.check(checks.is_owner)
    async def unload(self, ctx, name: str):
        """Unloads an extension."""
        try:
            ctx.bot.unload_extension("modules.{}".format(name))
        except Exception as e:
            await ctx.send(e)
            return
        e = discord.Embed(colour=discord.Colour.green())
        e.description = "Unloaded extention {}.py :ok_hand:".format(name)
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    @commands.check(checks.is_owner)
    async def load(self, ctx, name: str):
        """loads an extension."""
        try:
            ctx.bot.load_extension("modules.{}".format(name))
        except Exception as e:
            await ctx.send(e)
            return
        e = discord.Embed(colour=discord.Colour.green())
        e.description = "Loaded extention {}.py :ok_hand:".format(name)
        await ctx.send(embed=e)

    @commands.command()
    async def clean(self, ctx, max_messages: int=100):
        """Clean up the pixlz's messages."""
        if (max_messages > 100):
            raise errors.BadArgument("I cannot clean more that 100 messages at once.")

        can_mass_purge = ctx.channel.permissions_for(ctx.guild.me).manage_messages
        await ctx.channel.purge(limit=max_messages, check=lambda m: m.author == ctx.pixlz.user, before=ctx.message, after=datetime.datetime.now() - timedelta(days=14), bulk=can_mass_purge)
        await ctx.channel.purge(limit=max_messages, check=lambda m: m.content.startswith("p>"), before=ctx.message, after=datetime.datetime.now() - timedelta(days=14), bulk=can_mass_purge)
        await ctx.message.add_reaction('\u2705')

    @commands.command(pass_context=True)
    @commands.check(checks.is_owner)
    async def debug(self, ctx, *, code: str):
        """Evaluates code."""
        try:
            result = eval(code)
            if code.lower().startswith("print"):
                result
            elif asyncio.iscoroutine(result):
                await result
            else:
                msg = "```py\n"
                msg += "In: {}\n".format(code)
                msg += "Out: {}".format(result)
                msg += "```"
                await ctx.send(msg)
        except Exception as e:
            await ctx.send(wrap.format(type(e).__name__ + ': ' + str(e)))

def setup(pixlz):
   pixlz.add_cog(Dev(pixlz))
