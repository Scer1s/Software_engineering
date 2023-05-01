import discord
from discord import app_commands
from discord.ext import commands
import responses
import json
import sqlite3
#import requests
#from bs4 import BeautifulSoup


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(message, user_message)
        if response == "PROFANE":
            await message.delete()
        if response == 'Undef resp':
            pass
        else:
            await message.author.send(response) if is_private else await message.channel.send(response) #sends either to the channel or to the user
        
    except Exception as e:
        #print(e) for debugging
        pass



def run_discord_bot():
    with open('config.json', 'r') as cfg:
        data = json.load(cfg)
    TOKEN = data["BOTTOKEN"]
    print(TOKEN)
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!", intents = intents)

    @client.event #handles startup sequence and connects it to a database
    async def on_ready():
        print(f'{client.user} is locked and loaded B)')
        try:
            synced = await client.tree.sync()
            print(f"Synced {len(synced)} commands(s)")
        except Exception as e:
            print(e)

    @client.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!")
        

    @client.hybrid_command(description='Tells us the bot ping')
    async def ping(ctx):
        await ctx.send(f'Ping {round(client.latency *1000)}ms')

    @client.hybrid_command(description='Lists bot uses')
    async def bothelp(ctx):
        await ctx.send(f'This is school bot, a bot designed to help users in a verity of ways and has multipul commands that can be used that are listed below.'
                       'Another function of this bot is that it will take videos you post and store them in a database so even if you delete them they will still be in the database.'
                       'This is supposed to be a tool to help moderators catch people who upload inappropriate links and videos. So just be warned, Big Brother is watching you. Enjoy.\n \n'
                       'Response commands:\n hello\n roll\n -youtube\n -codehelp\n whoami\n \n'
                       'Slash commands:\n hello\n ping\n search\n')
        
        

    @client.tree.command(name="search")
    @app_commands.describe(search_argument = "What to search for?")
    async def search(ctx, search_argument: str):
        db = sqlite3.connect('message.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT Title, Link FROM Videos WHERE Message LIKE '%{search_argument}%'")
        rows = cursor.fetchall()
        result = ''
        for row in rows:
            result = result + row[0] + "\n" + row[1] + '\n'
            #print(row[0] + "\n" + row[1])
        await ctx.response.send_message(result)

    @client.event #handles messages
    async def on_message(message):
        if message.author == client.user: #stops the bot from looping on its own messages
            return

        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said:"{user_message}" in:({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        elif "https://www.youtube.com/watch?v=" in user_message:
            link_start_index = user_message.find("https://www.youtube.com/watch?v=") #Determines where the youtube link starts in the message
            msg_after_link = user_message[link_start_index:].split(" ", 1) #Separates the video link and the rest of the message
            youtube_link = msg_after_link[0] #Isolates the youtube link into one variable
            if not msg_after_link[1]:
                msg_without_link = user_message[:link_start_index] + "[LINK] " #Combines the messages
            else:
                msg_without_link = user_message[:link_start_index] + "[LINK] " + msg_after_link[1]
            r = requests.get(youtube_link) #The start of grabbing the title from the youtube link
            soup = BeautifulSoup(r.text, features="html.parser")
            link = soup.find_all(name="title")[0]
            youtube_title = str(link)
            youtube_title = youtube_title.replace("<title>","")
            youtube_title = youtube_title.replace("</title>","") #The end of grabbing the title, including formatting the title
            # print(youtube_link)
            # print(msg_without_link)
            # print(youtube_title)
            db = sqlite3.connect('message.sqlite')
            cursor = db.cursor()
            cursor.execute("INSERT INTO Videos (Channel, Name, Link, Title, Message) VALUES ( ?, ?, ?, ?, ?)", (channel, username, youtube_link, youtube_title, msg_without_link))
            db.commit()
            cursor.close()
            db.close()
            print("Youtube video saved to database")
        else:
            db = sqlite3.connect('message.sqlite') #Opens database
            cursor = db.cursor() #Creates cursor (cursors are used to place data into databases)
            cursor.execute("INSERT INTO Main (Channel, Name, Message) VALUES ( ?, ?, ?)", (channel, username, user_message)) #puts data into database
            db.commit() #commits changes
            cursor.close() #closes cursor (IMPORTANT)
            db.close() #closes database (IMPORTANT)
            await send_message(message, user_message, is_private=False)


    client.run(TOKEN)
