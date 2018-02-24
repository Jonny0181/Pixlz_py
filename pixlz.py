import discord
import traceback
import os
import sys
import asyncio
import config
import time
import datetime
from discord.ext import commands

start_time = time.time()
description = ""
def getPrefix(pixlz, msg):
    return commands.when_mentioned_or(*["P>", "p>", "Pixlz, "])(pixlz, msg)
pixlz = commands.AutoShardedBot(command_prefix=getPrefix, description=description)
pixlz.pm_help = None

modules = []

@pixlz.event
async def on_ready():
    global start_time
    start_time = time.time()
    guilds = len(pixlz.guilds)
    version = "v0.1"
    channels = len([c for c in pixlz.get_all_channels()])
    print("=================================================================")
    print(f'Logged in as: {pixlz.user.name}({pixlz.user.id})')
    print("Connected to       : {} guilds and {} channels".format(guilds, channels))
    print("=================================================================")
    print("Python Version     : {}.{}.{}".format(*os.sys.version_info[:3]))
    print("Discord.py Version : {}".format(discord.__version__))
    print("Pixlz Version   : {}".format(version))
    print("=================================================================")
    with open("logs/command_logs.txt", "w") as f:
        f.write("")
    await pixlz.change_presence(status=discord.Status.dnd, game=discord.Game(name="p>help | Currently in development!"))
    for mod in modules:
        try:
            pixlz.load_extention(mod)
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

@pixlz.event
async def on_command(ctx):
    server = "{0.id}/{0.name}".format(ctx.message.guild)
    msg = "[{0}] [Command] [{1}] [{2.author.id}/{2.author}]: {2.content}\n".format(time.strftime("%m/%d/%Y at %I:%M:%S %p %Z"), server, ctx.message)
    print(msg)
    with open("logs/command_logs.txt", "a") as f:
        f.write(msg)

@pixlz.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x: Missing a required argument. Help : ```css\n{0}{1:<{width}}\n\n{2}```".format(ctx.prefix, ctx.command.name, ctx.command.short_doc, width=5))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(":x: Bad argument provided. Help : ```css\n{0}{1:<{width}}\n\n{2}```".format(ctx.prefix, ctx.command.name, ctx.command.short_doc, width=5))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("{} :x:  You do not have permission to use this command.\nFor more information type `b!permissionshelp`.".format(ctx.message.author.mention))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(":x: This command is on cooldown. Try again in {:.2f}s".format(error.retry_after))
    elif isinstance(error, discord.Forbidden):
        await ctx.send("I dont have permissions to execute this command.")
    else:
        if ctx.command:
            if ctx.author.id == 170619078401196032:
                e = discord.Embed(title="Command threw an error!", description="An error has been thrown with this command!", colour=ctx.author.color)
                e.add_field(name="Command Name:", value=ctx.command.name, inline=False)
                e.add_field(name="Error:", value="{}".format(error), inline=False)
                e.add_field(name="Command Help:", value=ctx.command.help, inline=False)
                await ctx.send(embed=e)
            else:
                await ctx.send(":x: {} The command has thrown an error! Please join here to report it!\n**Invite Code:** `fmuvSX9`".format(ctx.author.mention))
        print('Ignoring exception in command {}'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@pixlz.command()
async def uptime(ctx):
    """Displays how long the bot has been online for"""
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    await ctx.send("I've been online for %d weeks, %d days, %d hours, %d minutes, %d seconds!" % (week, day, hour, minute, second))

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(pixlz.login(config.token))
    loop.run_until_complete(pixlz.connect())
except Exception:
    loop.run_until_complete(os.system("run.py"))
finally:
    loop.close()