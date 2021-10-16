import time
from botmodules import check
from botmodules.config import Guild
import discord
from discord.ext import commands
import json

class Bot(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.starttime = time.time()

    @commands.command()
    async def test(self,ctx):
        uptime = int(round(time.time()-self.starttime))
        ping = int(self.client.latency * 1000)
        await ctx.send(f'Botgach is running for {uptime} seconds, Latecy = {ping} ms') 

    @commands.command()
    @commands.check(check.is_dev)
    async def load(self,ctx,module:str):
        try:
            self.client.load_extension('Cogs.'+module)
        except Exception as e:
            print(e)
        else:
            print(module+' loaded.')

    @commands.command()
    @commands.check(check.is_dev)
    async def unload(self,ctx,module:str):
        try:
            self.client.unload_extension('Cogs.'+module)
        except Exception as e:
            print(e)
        else:
            print(module+' unloaded.')

    @commands.command()
    @commands.check(check.is_dev)
    async def reload(self,ctx,module:str):
        try:
            self.client.reload_extension('Cogs.'+module)
        except Exception as e:
            print(e)
        else:
            print(module+' reloaded.')
    @commands.command()
    @commands.check(check.is_dev)
    async def log(self,ctx):
        with open('config_log.json','w') as f:
            json.dump(Guild.config,f,indent=4)
        ag = {}
        for guild_id in Guild.active_guild:
            ag[guild_id] = {
                "command_prefix": Guild.active_guild[guild_id].command_prefix,
                "loop": Guild.active_guild[guild_id].loop,
                "voting": Guild.active_guild[guild_id].voting
            }
        with open('active_guild_log.json','w') as f:
            json.dump(ag,f,indent=4)




def setup(client):
    client.add_cog(Bot(client))