import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import sqlite3
import sys
import datetime
import asyncio
import pprint
import time

client = commands.Bot(command_prefix = '.')  #Bot command prefix such as .kick or .command

@client.event
async def on_ready():
	change_status.start()
	print('Bot is ready.')

  
  client.run('NjM1ODc3NjcxNzgzNjI4ODE0.Xa3dOg.iwsKYUnQZNFsugzVlG2-fBKuYy8') #Botkey
