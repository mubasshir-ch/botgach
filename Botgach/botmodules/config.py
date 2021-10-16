import pickle
import discord
from discord.ext import commands

DEFAULT_PREFIX = '&'

class Guild:
    default_prefix = '&'
    config = {}
    active_guild = {}

    @classmethod
    def load_config(cls,path='config.dat'):
        try:
            with open(path,'rb') as f:
                cls.config = pickle.load(f)
        except FileNotFoundError:
            with open(path,'wb') as f:
                pickle.dump(cls.config,f)
    
    @classmethod
    def save_config(cls,path='config.dat'):
        with open(path,'wb') as f:
            pickle.dump(cls.config,f)

    @classmethod
    def load_guild(cls,id:str):
        id = str(id)
        guild_info = cls.config['guilds'][id]
        cls.active_guild[id] = Guild(id ,guild_info['command_prefix'],guild_info['voting'],guild_info['loop'])
        return cls.active_guild[id]

    @classmethod
    def get_guild(cls,id:str):
        id=str(id)
        return cls.active_guild[id]

    @classmethod
    def get_prefix(cls,client,message):
        if not message.guild:
            return DEFAULT_PREFIX
        id = str(message.guild.id)
        return cls.get_guild(id).command_prefix

    @classmethod
    def new_guild(cls,id:str):
        id=str(id)
        guild = Guild(id)
        cls.active_guild[id] = guild
        cls.config['guilds'][id] = {
            'command_prefix': guild.command_prefix,
            'voting': guild.voting,
            'loop': guild.loop
        }
        cls.save_config()
        return guild
    
    @classmethod
    def remove_guild(cls,id:str):
        cls.active_guild.pop(id)
        cls.config['guilds'].pop(id)
        cls.save_config()

    def __init__(self,id:str , command_prefix = DEFAULT_PREFIX, voting = False , loop = "none") :
        self.id = id
        self.command_prefix = command_prefix
        self.votes = {
            "skip": set(),
            "clear": set(),
            "leave": set()
        }
        self.voting = voting
        self.now_playing = None
        self.loop = loop.lower() # none, one , all
        self.queue = []
        self.last= None

    def is_adder(self,user) :
        return self.now_playing.added_by == user

    def change_prefix(self,prefix:str):
        self.command_prefix = prefix
        Guild.config['guilds'][self.id]['command_prefix'] = prefix
        Guild.active_guild[self.id].command_prefix = prefix
        Guild.save_config()

    def change_voting(self,state:bool):
        state = bool(state)
        self.voting = state
        Guild.config['guilds'][self.id]['voting'] = state
        Guild.active_guild[self.id].voting = state
        Guild.save_config()

    def voting_status(self):
        return 'Voting is on' if self.voting else 'Voting is off'

    def loop_status(self):
        if self.loop == "none":
            return "Looping is turned off"
        elif self.loop == "one":
            return "Looping one song"
        else:
            return "Looping all songs"

    def change_loop(self,state):
        state=state.lower()
        self.loop = state
        Guild.config['guilds'][self.id]['loop'] = state
        Guild.active_guild[self.id].loop = state
        Guild.save_config()



