from os import error
import discord
from discord.ext import commands
from discord.ext.commands.core import command
from discord.ext.commands.errors import BadArgument, CommandError, CommandNotFound, MissingRequiredArgument

class Error(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if hasattr(ctx.command,"on_error"):
            return
        
        error = getattr(error,'original',error)
        prefix = ctx.bot.command_prefix(ctx.bot,ctx.message)
    
        if isinstance(error,CommandNotFound):
            return await ctx.send(f"{ctx.author.mention}, your command doesn't exist. Use `{prefix}help` for a list of commands")

        if isinstance(error,MissingRequiredArgument):
            return await ctx.send(f'{ctx.author.mention} Please provide required arguments')

        # if isinstance(error,BadArgument):
        #     if ctx.command.name=="play":
        #         return 
        #     return await ctx.send(f'{ctx.author.mention} Make sure your arguments are in correct format')

        if isinstance(error, CommandError):
            return await ctx.send(f'Error while executing command `{ctx.command.name}` : {str(error)}')
        await ctx.send(f'Unexpected Error on command `{ctx.command.name}` : ```{str(error)}``` Please contact the dev (hackermub#7460)' )
        raise error

def setup(client):
    client.add_cog(Error(client))
