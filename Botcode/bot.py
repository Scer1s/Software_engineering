import discord
from discord.ext import commands, tasks
from itertools import cycle
import sys
import asyncio
import pprint


client = commands.Bot(command_prefix = '.')  #Bot command prefix such as .kick or .command

@client.event
async def on_ready():
	change_status.start()
	print('Bot is ready.')

#CODE GOES HERE
  
  client.run('NjM1ODc3NjcxNzgzNjI4ODE0.Xa3dOg.iwsKYUnQZNFsugzVlG2-fBKuYy8') #Botkey (replace with secret botkey)
