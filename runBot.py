import os, sys, time
import importlib
import logging
import json

import tweepy

from configuration import *
from secrets import *

param = dict()

######### Logging ##################

logger = logging.getLogger("MARTA")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(bot_username + '.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

######### Twitter Interface ##################

def get_api():
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    return tweepy.API(auth)

def get_dms(api):
    lastdm = param.get('lastdm', None)
    dmlist = None
    try:
        dmlist = api.direct_messages(lastdm)
    except tweepy.error.TweepError as e:
        logger.error(e.message)
    else:
        logger.info("Loaded "+str(len(dmlist))+" direct messages")
        if len(dmlist) > 0:
            param['lastdm'] = dmlist[0].id
            dmlist.reverse()
    return dmlist

def get_timeline(api):
    lasttl = param.get('lasttimeline', None)
    tl = None
    try:
        tl = api.home_timeline(lasttl)
    except tweepy.error.TweepError as e:
        logger.error(e.message)
    else:
        logger.info("Loaded "+str(len(tl))+" timeline messages")
        if len(tl) > 0:
            param['lasttimeline'] = tl[0].id
            tl.reverse()
    return tl


def tweet(api, text, replyid = None):
    """Send out the text as a tweet."""
    # Send the tweet and log success or failure
    try:
        api.update_status(text, replyid)
    except tweepy.error.TweepError as e:
        logger.warning("Failed to tweet with error: "+str(e))
    else:
        logger.info("Tweeted: " + text)

######### Utilities ##########################
def loadstate():
    try:
        fd = open(bot_username+".state")
        param.update(json.load(fd))
    except:
        e = sys.exc_info()[0]
        logger.error("Reading state file: "+str(e))
    else:
        logger.info("Loaded state file "+bot_username+".state")
        fd.close()

def savestate():
    fd = open(bot_username+".state","w")
    json.dump(param,fd)
    fd.close()

def powerswitch(dms): # Returns true if the robot must turn off.
    for dm in dms:
        if (dm.sender_screen_name == bot_owner):
            if dm.text == 'start':
                param['stopped'] = False
                logger.info("Got a DM telling me to start (id "+str(dm.id)+")")
            if dm.text == 'stop':
                param['stopped'] = True
                logger.info("Got a DM telling me to stop (id "+str(dm.id)+")")
    return (param.get('stopped',False))

######## Main #################################
    
def run_bot():

    loadstate()
    api = get_api()
    
    # Get DMs and Timeline, check if I can run
    dms = get_dms(api)

    if powerswitch(dms):
        logger.info("Bot set to freeze. Stopping")
        savestate()
        return
    
    timeline = get_timeline(api)
    
    # Running Modules
    for mod in modules:
        m = importlib.import_module("modules."+mod)
        modparam = param.get(mod,{})
        if "update" in dir(m):
            logger.debug("Updating module "+mod)
            tweets, modparam = m.update(modparam, api, dms, timeline)
            param[mod] = modparam
            for t in tweets:
                tweet(api,t.get("text",None),t.get("reply",None))
        else:
            logger.warning("No update function on module "+mod)
                
    
    # Close program and save state    
    param['lastran'] = round(time.time())
    savestate()

if __name__ == "__main__":
    run_bot()
