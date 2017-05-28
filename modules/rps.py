import time, random, math
import logging

from configuration import bot_username

logger = logging.getLogger("MARTA")

hands = ('rock','paper','scissors')


def selectplay():
    return random.randint(0,2)

def update(param, api, dms, timeline):
    messages = []

    for i in timeline:
        sender = i.author.screen_name
        text = i.text.lower()
        m_id = i.id
        
        if ("#rps" in text) and (sender != bot_username):
            reply = {}
            reply["reply"] = m_id
            
            played = 0
            for j in range(0,3):
                if hands[j] in i.text.lower():
                    played |= (1 << j)
            if played == 0:
                reply["text"] = "@" + sender + " let's play! Send me one of rock/paper/scissors #rps"
            elif (played == 1) or (played == 2) or (played == 4):
                player_game = int(math.log(played,2))
                bot_game = selectplay()
                reply["text"] = "@" + sender + " you played " + hands[player_game] + ", I played " + hands[bot_game] + ". "
                if (player_game == bot_game):
                    reply["text"] = reply["text"] + "It's a tie! #rps"
                if ((player_game + 1) % 3 == bot_game):
                    reply["text"] = reply["text"] + "I win! #rps"
                if ((player_game - 1) % 3 == bot_game):
                    reply["text"] = reply["text"] + "You win! #rps"
            else:
                reply["text"] = "@" + sender + " come on, choose only one! #rps"
            messages.append(reply)
    
        
    return messages, param
