import discord
from discord.ext import commands
import Player as pl
import contextlib
import asyncio
import wave
import os

TOKEN = 'TOKEN'
client = commands.Bot(command_prefix='-')
player = None

## COMMANDS
# SKIP COMMAND
@client.command()
async def skip(ctx):
    try:
        player.timer.cancel()
        await player.next()
    except:
        print("ERROR: Cannot call 'skip' function.")
        return

# ON_READY EVENT
@client.event
async def on_ready():
    global player

    if not os.path.exists('music'):
        os.mkdir('music')


    player = pl.Player()

# P COMMAND
@client.command()
async def p(ctx, url):
    try:
        channel = ctx.author.voice.channel
    except:
        max = 0
        for guild in client.guilds:
            for channels in guild.channels:
                if channels.type == discord.ChannelType.voice and max < len(channels.members):
                    max = len(channels.members)
                    channel = channels

    try:
        if player.is_connected == False:
            await channel.connect()
            player.player = ctx.voice_client
            player.is_connected = True
        await player.download(url)
    except:
        print("ERROR: There is no user's voice client. And nobody connected.")

@client.command()
async def remove(ctx):
    await player.remove()

# LEAVE COMMAND
@client.command()
async def leave(ctx):
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    player.__del__()

client.run(TOKEN)