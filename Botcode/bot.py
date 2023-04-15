import discord
from discord import app_commands
from discord.ext import commands
import responses
import json


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
    client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

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
            msg_without_link = user_message[:link_start_index] + "[LINK] " + msg_after_link[1] #Combines the message before and after the youtube link into one string
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
            await send_message(message, user_message, is_private=False)


    client.run(TOKEN)
