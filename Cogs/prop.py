import os,sys,inspect
from discord import client

from discord.ext.commands.core import command
from discord.ext.commands.errors import BadArgument, CommandError
from youtube_dl.utils import cli_bool_option
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from botmodules import check
from botmodules.config import Guild
import discord
from discord.ext import commands

class Prop(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        id = str(guild.id)
        g = Guild.new_guild(id)
        user = await guild.fetch_member(Guild.config['BOT_ID'])
        await user.edit(nick=f'[{g.command_prefix}] বটগাছ')

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        id = str(guild.id)
        Guild.remove_guild(id)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if not before.channel:
            return 
        G = before.channel.guild
        guild = Guild.get_guild(G.id)
        if member==self.client.user:
            guild.queue=[]
            return 
        if not G.voice_client:
            return
        voice = G.voice_client.channel 
        if before.channel and before.channel==voice:
            if not after.channel:
                tot = len([member for member in voice.members if not member.bot])
                if not tot:
                    if not G.voice_client.is_paused():
                        G.voice_client.pause()
                        await guild.last.send('All user left. Pausing audio')

    @commands.command(brief='Change command prefix for this bot, Admin-only command',aliases=['cp'])
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def changeprefix(self,ctx,prefix:str):
        id = str(ctx.guild.id)
        guild = Guild.get_guild(id)
        guild.change_prefix(prefix)
        user = await ctx.guild.fetch_member(Guild.config['BOT_ID'])
        await user.edit(nick=f'[{prefix}] বটগাছ')
        await ctx.send('Command prefix changed to '+prefix)

    @commands.command()
    @commands.guild_only()
    async def voting(self,ctx,state="show"):
        state=state.lower()
        id = str(ctx.guild.id)
        guild = Guild.get_guild(id)
        if(state=="show"):
            return await ctx.send(guild.voting_status())
        if state!="off" and state!="on":
            raise BadArgument

        if ctx.author.guild_permissions.administrator:
            guild.change_voting(state=="on")
            await ctx.send('Voting turned '+state)
        else:
            raise CommandError('Only admins can change voting state')
    


def setup(client):
    client.add_cog(Prop(client))