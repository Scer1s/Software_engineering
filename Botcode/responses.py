import random
import discord

msglist = ["Bababooey",
           "How can I help?",
           "Whoever programmed me needs help",
           "bruh",
           "HELLO",
           "awa",
           "UwU",
           "Hi!",
           "What?",
           "No way",
           "Discord is cool"]
    

def get_response(ctx, message): #gets the response from defined code
    p_message = message.lower()

    if p_message == 'hello':
        return 'Sup'
    elif p_message == 'roll':
        return str(random.randint(1,6))
    elif p_message == '-youtube':
        return 'https://www.youtube.com/'
    elif p_message == '-codehelp':
        return 'https://www.geeksforgeeks.org/', 'https://stackoverflow.com/', 'https://www.tutorialspoint.com/index.htm', 'https://www.w3schools.com/'
    elif p_message == '!help':
        return 'Help message deployed'
    elif p_message == 'whoami':
        result = (f'You are {ctx.author.mention}. \nYou joined Discord on {ctx.author.created_at.strftime("%a, %b %#d, %Y")}\nYou joined this server on {ctx.author.joined_at.strftime("%a, %b %#d, %Y")}')
        return result
    else:
        if(random.randint(0,20) <= 1):
            choice = random.choice(msglist)
            print(choice)
            return choice
    
    return


