import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init(self,client):
        self.client = client

    
def setup(client):
    client.add_cog(Help(client))