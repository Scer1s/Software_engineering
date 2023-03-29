import discord
import responses



async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if response == 'Undef resp':
            pass
        else:
            await message.author.send(response) if is_private else await message.channel.send(response) #sends either to the channel or to the user
        
    except Exception as e:
        pass


def run_discord_bot(): #DELETE TOKEN BEFORE PUSHING TO GITHUB AND PUT IT BACK IN BEFORE TESTING
    TOKEN = '' #DO NOT POST THIS ANYWHERE
    intents = discord.Intents.all() #intents are new security features in discord, ask sceris before fucking with this
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event #handles startup sequence
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
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
