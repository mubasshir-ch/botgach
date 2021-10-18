import discord
from discord.ext import commands
import youtube_dl
from datetime import datetime

def get_op(start=40):
    ytd_op = {
        'verbose': True,
        'format': 'mp4',
        'default_search': 'ytsearch',
        'quite': 'True',
        'cookiefile': 'cookies.txt',
        'options': f'-vn -ss {start}'
    }
    return ytd_op

class Video:

    def __init__(self,search,addeb_by):
        vid = self.info(search)
        if vid=="VideoNotFound":
            self.found = False
            return
        self.found = True
        self.title = vid['title']
        self.play_url = vid['formats'][0]['url']
        self.web_url = vid['webpage_url']
        self.duration = int(vid['duration']) if 'duration' in vid else None
        self.uploader = vid['uploader'] if 'uploader' in vid else None
        self.thumbnail = vid['thumbnail'] if 'thumbnail' in vid else None
        self.added_by = addeb_by

    def info(self,search):
        with youtube_dl.YoutubeDL(get_op()) as ytd:
            try:
                lst = ytd.extract_info(search,download=False)
            except youtube_dl.utils.DownloadError:
                return "VideoNotFound"
            else:
                if '_type' in lst and lst['_type']=='playlist':
                    if len(lst['entries'])==0:
                        return "VideoNotFound"
                    return self.info(lst['entries'][0]['webpage_url'])
                return lst

    def get_embed(self,title):
        embed = discord.Embed(title=title,
            description=f'[{self.title}]({self.web_url})',
            icon=self.added_by.avatar_url,
            color = 0x4287f5 )
        
        if self.uploader!=None:
            embed.add_field(name='Uploader',value=f'`{self.uploader}`',inline=True)
        if self.duration!=None:
            embed.add_field(name='Duration',value=f'`{self.get_duration()}`',inline=True)

        embed.add_field(name='Added by',value=self.added_by.mention,inline=True)
        if self.thumbnail!=None:
            embed.set_thumbnail(url=self.thumbnail)
        return embed
        

    def get_duration(self,dur=0):
        if not dur:
            if hasattr(self,"duration"):
                dur=self.duration
        if dur>=3600:
            return datetime.strftime(datetime.fromtimestamp(dur),"%H:%M:%S")
        return datetime.strftime(datetime.fromtimestamp(dur), "%M:%S")

