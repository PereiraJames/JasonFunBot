import os
import json
from bully import bully
import jasontools


BOTTOKEN = jasontools.parseEnvFile("BOT_TOKEN")
BOT_USERNAME = jasontools.parseEnvFile("BOT_USERNAME")

MASTER_USERNAME = jasontools.parseEnvFile("TELE_MASTERNAME")
MASTER_ID = jasontools.parseEnvFile("TELE_MASTERID")
HERMES_ID = jasontools.parseEnvFile("TELE_HERMESID")
TELE_DRANKSID = jasontools.parseEnvFile("TELE_DRANKSID")

userstates = {}

def readCommandList(master=False):
    
    with open('commands.json') as file:
        data = json.load(file)
    
    # print(data)

    if master:
        commandlist = data['mastercommands']

    else:
        commandlist = data['commands']

    allcommands = ""
        
    for command in commandlist:
        allcommands += f"{command} | {commandlist[command]}" + "\n"

    print(allcommands)
    
readCommandList(False)

# token = jasontools.parseEnvFile("OPENAI_KEY")

# test = jasontools.parseEnvFile("STORY_DB_CONFIG")

# print(token)
# print(test)
# print(type(test))
# print(test['host'])

