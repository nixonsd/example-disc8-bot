import discord
from discord.ext import commands
import Player as pl
import contextlib
import asyncio
import os

TOKEN = 'NzA5Njk5NjkyOTEyNzA1NjQ2.XrptWA.ShYcyMLgU51q72LMKzm4kLaJl5k' # TOKEN
client = commands.Bot(command_prefix='-')
player = None

## COMMANDS

# ON_READY EVENT - CHECKED
@client.event
async def on_ready():
    global player
    player = pl.Player()

# SKIP COMMAND
@client.command()
async def skip(ctx):
    try:
        player.timer.cancel()
        await player.next()
    except:
        print("ERROR: Couldn't invoke skip function.")
        return

# P COMMAND
@client.command()
async def p(ctx, url):
    try:
        if player.invoked != True:
            channel = ctx.author.voice.channel
            await channel.connect()
            player.voice = ctx.voice_client
            player.invoked = True
        try:
            await player.download(url)
        except:
            print("ERROR: Couldn't find the video.")
    except:
        print("ERROR: Couldn't invoke play function.")

#@client.command()
#async def remove(ctx):
#    await player.remove()

# LEAVE COMMAND
@client.command()
async def leave(ctx):
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    player.__del__()

client.run(TOKEN)