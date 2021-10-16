import os,sys,inspect

from discord.ext.commands.errors import CommandError
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import discord
from discord.ext import commands
from . import config
from Cogs import error

def is_dev(ctx):
    return str(ctx.author.id) == config.Guild.config['DEV_ID']

# definitely didn't copy these codes from joek13/py-music-bot

async def audio_playing(ctx):
    client = ctx.guild.voice_client
    if client and client.channel and client.source:
        return True
    raise CommandError('No audio is playing')

async def in_voice_channel(ctx):
    author_voice = ctx.author.voice
    bot_voice = ctx.guild.voice_client

    if author_voice and author_voice.channel:

        if bot_voice and bot_voice.channel:

            if author_voice.channel==bot_voice.channel:
                return True
            if bot_voice.source:
                raise CommandError('Already playing in a different voice channel')
            else:
                return True
        else:
            return True
    else:
        raise CommandError('You need to be in a voice channel')
    
async def is_audio_adder(ctx):
    guild = config.Guild.get_guild(ctx.guild.id)
    vid = guild.now_playing
    is_admin = ctx.channel.permissions_for(ctx.author).administrator
    if vid and vid.added_by==ctx.author or is_admin or not guild.vote_skip:
        return True
    raise CommandError('You are not the song requester or the admin')


