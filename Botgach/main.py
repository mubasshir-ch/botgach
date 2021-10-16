import discord
from discord.ext import commands
from botmodules.config import Guild
import asyncio

#BOT CODES
intents = discord.Intents().all()
client = commands.Bot(command_prefix = Guild.get_prefix, intents=intents)

COGS = ['Cogs.bot','Cogs.song','Cogs.prop','Cogs.error','Cogs.help']

async def load_guilds():
    async for guild in client.fetch_guilds():
        g=Guild.load_guild(str(guild.id))
        user = await guild.fetch_member(Guild.config['BOT_ID'])
        await user.edit(nick=f'[{g.command_prefix}] বটগাছ')

async def constant_ping():
    await asyncio.sleep(60)

@client.event
async def on_ready():
    await load_guilds()
    print('Botgach is ready to roll!')

if __name__== '__main__':
    Guild.load_config()
    for cog in COGS:
        client.load_extension(cog)
    client.loop.create_task(constant_ping())
    client.run(Guild.config['BOT_TOKEN'])