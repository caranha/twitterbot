import time
import random
import logging

logger = logging.getLogger("MARTA")

nicethings = [
    "Thanks for building me!",
    "Programming is fun!",
    "What you make is important!",
    "Be silly!",
    "Always look on the bright side of life!",
    "Maybe I'll be alive someday!",
    "Time for a deep breath",
    "Let's play \#RPS from time to time"
    ]


def update(param, api, dms, timeline):
    last = param.get("lastmessage",0)
    now = round(time.time())
    nextm = param.get("nextmessage",random.randint(3600,10000))
    message = []
    
    if (now - last) > nextm and time.localtime().tm_hour > 7:
        message.append({"text" : "@caranha " + nicethings[random.randint(0,len(nicethings)-1)]})
        param["lastmessage"] = now
        param["nextmessage"] = random.randint(3600,10000)
        logger.info("Sending new message: " + message[0]["text"])
    else:
        logger.info("Too early to send messages. Next message in "+str(last+nextm - now))
        
    return message, param
