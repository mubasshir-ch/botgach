import os,sys,inspect
from discord import channel

from discord.errors import ClientException
from discord.ext.commands.core import command, guild_only
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import discord
from discord.ext import commands
from botmodules.config import Guild
from botmodules import check,config
from botmodules.video import Video


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

async def lmao(ctx):
    raise commands.CommandError('what the fuck')

class Song(commands.Cog):

    def __init__(self,client):
        self.client = client

    def play_song(self,client,guild_id):
        guild = config.Guild.get_guild(guild_id)
        guild.votes = {
            "skip": set(),
            "clear": set(),
            "leave": set()
        }
        if not len(guild.queue):
            guild.now_playing = None
            return
        vid = guild.queue[0]
        guild.now_playing = vid
        def after_song(err):
            if not len(guild.queue):
                guild.now_playing = None
                return
            if err: print(str(err))
            guild.now_playing = None
            if guild.loop == "one":
                self.play_song(client,guild_id)
            else:
                guild.queue.pop(0)
                if guild.loop == "all":
                    guild.queue.append(vid)
                if len(guild.queue):
                    self.play_song(client,guild_id)

        client.play(discord.FFmpegPCMAudio(vid.play_url,**FFMPEG_OPTIONS) , after = after_song)

    async def add_song(self,ctx,arg,voice):
        vid = Video(arg,ctx.author)
        if not vid.found:
            await ctx.send('No result found for '+arg)
            return
        guild = Guild.get_guild(ctx.guild.id)
        guild.last = ctx
        guild.queue.append(vid)
        await ctx.send(embed=vid.get_embed('Added Song'))
        if not guild.now_playing :
            self.play_song(voice,str(ctx.guild.id))
        else:
            await ctx.send('Resuming Paused Audio')
            ctx.guild.voice_client.resume()

    @commands.command(aliases=['p','add'])
    @commands.guild_only()
    @commands.check(check.in_voice_channel)
    async def play(self,ctx,*,arg=""):
        if arg=="":
            return await self.pause(ctx)
        try:
            voice = await ctx.author.voice.channel.connect()
        except ClientException:
            voice = ctx.guild.voice_client
        await ctx.send(ctx.author.mention+' Searching...')
        await self.add_song(ctx,arg,voice)

    @commands.command(aliases=['resume'])
    @commands.guild_only()
    @commands.check(check.audio_playing)
    async def pause(self,ctx):
        voice = ctx.guild.voice_client
        self.pause_song(voice)


    def pause_song(self,client):
        if client.is_paused():
            client.resume()
        else:
            client.pause()

    @commands.command(aliases=['np','now'])
    @commands.guild_only()
    @commands.check(check.audio_playing)
    async def now_playing(self,ctx):
        g = Guild.get_guild(ctx.guild.id)
        await ctx.send(embed = g.now_playing.get_embed('Now playing'))

    def queue_page(self,ctx,page):
        guild = Guild.get_guild(ctx.guild.id)
        embed = discord.Embed(title = f'Playlist of `{ctx.guild.name}`',description=f'`{guild.loop_status()}` \t`{guild.voting_status()}` \n`Total songs:{len(guild.queue)}`' ,color = 0x4287f5)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        total = len(guild.queue)
        total_page = (total-1)//5
        page = page-1
        page = min(page,total_page)
        page = max(page,0)
        st = page*5

        idx = 0
        tot_dur = 0
        while idx<st:
            dur = guild.queue[idx].duration
            if not dur:
                dur = 0
            tot_dur = tot_dur + dur
            idx = idx+1
        
        while idx<(st+5) and idx<total:
            vid = guild.queue[idx]
            pidx = str(idx) if idx else "Now Playing"
            value = f'`{pidx}` [{vid.title}]({vid.web_url})'
            embed.add_field(name='\u200b',value=value , inline=False)
            if vid.uploader!=None:
                embed.add_field(name='Uploader',value=f'`{vid.uploader}`',inline=True)
            if vid.duration!=None:
                embed.add_field(name='Duration',value=f'`{vid.get_duration()}`',inline=True)
            embed.add_field(name='Added by',value=vid.added_by.mention,inline=True)
            if idx:
                embed.add_field(name='Est. until playing',value = f'`{vid.get_duration(tot_dur)}`',inline=True)
            tot_dur=tot_dur + vid.duration
            idx=idx+1
        
        page_info = f"Showing page {page+1} of {total_page+1}." 
        command_help = f"Use `{guild.command_prefix}queue PageNo` for a specific page." 
        full_help = f"`{guild.command_prefix}queue 0` for full playlist"
        embed.description= embed.description + '\n\n' + command_help + full_help
        embed.set_footer(text = page_info)
        return embed

    @commands.command(aliases=["q","playlist"])
    @commands.guild_only()
    async def queue(self,ctx,page=1):
        guild = config.Guild.get_guild(ctx.guild.id)
        total = len(guild.queue)
        total_page = (total-1)//5
        if not total:
            await ctx.send('The queue is empty')
        else:
            if page:
                await ctx.send(embed=self.queue_page(ctx,page))
            else:
                while page<=total_page:
                    print(page)
                    await ctx.send(embed=self.queue_page(ctx,page+1))
                    page = page+1

    async def skip_song(self,ctx):
        voice = ctx.guild.voice_client
        voice.stop()
        guild = Guild.get_guild(ctx.guild.id)
        guild.now_playing = None
        vid = guild.queue[0]
        if guild.loop=="One":
            guild.queue.pop(0)
        await ctx.send(embed = vid.get_embed('Skipping Song'))
    
    async def clear_queue(self,ctx,silent=False):
        guild = Guild.get_guild(ctx.guild.id)
        guild.queue=[]
        voice = ctx.guild.voice_client
        voice.stop()
        if not silent: await ctx.send('Cleared Queue')

    async def leave_channel(self,ctx):
        voice = ctx.guild.voice_client
        await voice.disconnect()

    async def vote(self,ctx,vote_type,success):
        channel = ctx.author.voice.channel
        guild = Guild.get_guild(ctx.guild.id)
        is_admin = ctx.channel.permissions_for(ctx.author).administrator
        if (not guild.voting) or is_admin or (guild.now_playing and ctx.author==guild.now_playing.added_by):
           await success(ctx)
        else:
            print(vote_type,type(guild.votes[vote_type]))
            guild.votes[vote_type].add(ctx.author)
            total = len([member for member in channel.members if not member.bot])
            votes_count = len(guild.votes[vote_type])
            req = (total+1)//2
            if votes_count<req:
                await ctx.send(f"`{votes_count}` voted to {vote_type}, `{req}` required.")
            else:
                await success(ctx)

    @commands.command(aliases=["c"])
    @commands.check(check.in_voice_channel)
    @commands.guild_only()
    async def clear(self,ctx):
        await self.vote(ctx,"clear",self.clear_queue)

    @commands.command(aliases=["stop"])
    @commands.guild_only()
    @commands.check(check.in_voice_channel)
    async def leave(self,ctx):
        await self.vote(ctx,"leave",self.leave_channel)

    @commands.command(aliases=['s'])
    @commands.guild_only()
    @commands.check(check.in_voice_channel)
    @commands.check(check.audio_playing)
    async def skip(self,ctx):
        await self.vote(ctx,"skip",self.skip_song)

    @commands.command(aliases=['l'])
    @commands.guild_only()
    async def loop(self,ctx,state=""):
        loop_options = ["none","all","one"]
        guild = Guild.get_guild(ctx.guild.id)
        state=state.lower()
        if state=="":
            await ctx.send(guild.loop_status() + '. Loop states: ' + str(loop_options))
        elif state in loop_options:
            guild.change_loop(state)
            await ctx.send(guild.loop_status())
        else:
            await ctx.send(f"Please write loop state correctly.`{str(loop_options)}`")

    @commands.command(aliases=['m'])
    @commands.guild_only()
    async def move(self,ctx,current:int,target:int):
        guild = Guild.get_guild(ctx.guild.id)
        current = int(current)
        target = int(target)
        if current==target:
            return await ctx.send(f'{ctx.author.mention} successfully done nothing. \U0001F44D')

        mx = max(current,target)
        mn = min(current,target)
        
        if mn<1 or mx>=len(guild.queue):
            if not current:
                return await ctx.send('Cannot move currently playing song')
            return await ctx.send(f'Enter valid positions `1 to {len(guild.queue)-1}`')
        
        vid = guild.queue.pop(current)
        guild.queue.insert(target,vid)
        await ctx.send(f'Moved `{vid.title}` to position `{target}`')

    @commands.command(aliases=['r'])
    @commands.guild_only()
    @commands.check(check.audio_playing)
    async def remove(self,ctx,idx):
        guild = Guild.get_guild(ctx.guild.id)
        tot = len(guild.queue)-1
        idx = int(idx)
        if not idx:
            return await ctx.send('Use skip command to remove currently playing song')
        if idx>tot:
            return await ctx.send('Enter a valid position. `1 to {tot}`')
        vid = guild.queue[idx]
        is_admin = ctx.channel.permissions_for(ctx.author).administrator
        if vid.added_by==ctx.author or is_admin or not guild.vote_skip:
            guild.queue.pop(idx)
            await ctx.send(f'Song `{vid.title}` removed from queue')
        else:
            await ctx.send('You have to be the admin or the song adder to do that.')
        

def setup(client):
    client.add_cog(Song(client))