import random

def get_response(message: str ) -> str: #gets the response from defined code
    p_message = message.lower()

    if p_message == 'hello':
        return 'Sup'

    if p_message == 'roll':
        return str(random.randint(1,6))

    if p_message == '-youtube':
        return 'https://www.youtube.com/'

    if p_message == '!help':
        return 'Help message deployed'

    return
