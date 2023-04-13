import discord
import responses
import json
import sqlite3

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(message, user_message)
        if response == 'Undef resp':
            pass
        else:
            await message.author.send(response) if is_private else await message.channel.send(response) #sends either to the channel or to the user
        
    except Exception as e:
        #print(e) for debugging
        pass

def run_discord_bot(): #DELETE TOKEN BEFORE PUSHING TO GITHUB AND PUT IT BACK IN BEFORE TESTING
    with open('config.json', 'r') as cfg:
        data = json.load(cfg)
    TOKEN = data["BOTTOKEN"]
    print(TOKEN)
    
    intents = discord.Intents.all() #intents are new security features in discord, ask sceris before fucking with this
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event #handles startup sequence and connects it to a database
    async def on_ready():
        print(f'{client.user} is locked and loaded B)')


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
        else:
            db = sqlite3.connect('message.sqlite')
            cursor = db.cursor()
            cursor.execute("INSERT INTO Main (Channel, Name, Message) VALUES ( ?, ?, ?)",
		(channel, username, user_message))
            db.commit()
            cursor.close()
            db.close()
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
