import random
import discord

def get_response(ctx, message): #gets the response from defined code
    p_message = message.lower()

    if p_message == 'hello':
        return 'Sup'

    if message == 'roll':
        return str(random.randint(1,6))

    if p_message == '!help':
        return 'Help message deployed'

    if p_message == 'whoami':
        result = (f'You are {ctx.author.mention}. \nYou joined Discord on {ctx.author.created_at.strftime("%a, %b %#d, %Y")}\nYou joined this server on {ctx.author.joined_at.strftime("%a, %b %#d, %Y")}')
        return result
    return
