import random
def handle_responses(message) -> str:
    p_message = message[1:].lower()

    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))

    if p_message[:4] == 'kiss':         #was a test to try emojis
        message = p_message.split()
        try:
            return f'{message[1]} :kiss: '
        except IndexError as e:
            return '```The correct syntax is : ?kiss @<person/bot>```'
    
    if p_message == 'weather':
        return '```The syntax is: ?weather [city_name]```'
    
    if p_message == 'convert':
        return '```The syntax is ?convert [from_currency] [to_currency] [amount]``` \n**If you wish to know the currencies you can convert to and from, use:** ```?currencies```'
        
    
