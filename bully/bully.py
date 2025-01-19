import random
import csv
import datetime
import os
import jasontools
import asyncio
from openai import OpenAI
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext 

BULLYSTATE = True

BULLYTOLERANCE = 10

import mysql.connector
import jasontools

db_config = jasontools.parseEnvFile("DB_CONFIG")

def insertUser(username,userid,whitelisted="None",blacklisted="None",realname="nameless"):
    
    query = """
        INSERT INTO telegramUsers (username, userid, whitelisted, blacklisted, realname)
        VALUES (%s,%s,%s,%s,%s)
    """

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    cursor.execute(query, (
        username, userid, whitelisted, blacklisted, realname
    ))
    
    print(f"Imported {username} | {realname} | {userid}")

    db.commit()

def findUser(username):
    
    query = """
        SELECT *
        FROM telegramUsers
        WHERE username = (%s)
    """

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    cursor.execute(query, (username,))

    response = cursor.fetchall()

    userData = []

    for row in response:
        rowData = {
            "id" : row[0],
            "username" : row[1],
            "userid" : row[2],
            "whitelistsed" : row[3],
            "blacklisted" : row[4],
            "realname" : row[5],
            "profileDesc" : row[6]
        }

        userData.append(rowData)

    cursor.close()
    db.close()

    if userData:
        return userData
    else:
        return False


def updateUser(username,userid):

    if findUser(username):
        print("Already in database")
        return False
    else:
        insertUser(username,userid)
        return True


def getInsult(targetsUsername):
    if BULLYSTATE == False:
        return None

    userdetails = findUser(targetsUsername)

    if len(userdetails) != 1:
        print(f"Found {len(userdetails)} in database.")
        return None
    else:
        print(userdetails)

        user_realname = userdetails[0]['realname']
        user_profileDesc = userdetails[0]['profileDesc']

        generatedInsult = generateInsult(user_realname, user_profileDesc)

        return generatedInsult

def generateInsult(realname,userDesc):
    chat_prompt = f"Create a short insult for my friend {realname} using this short description of him. You do not need to use all these details, just pick one and make an insult. {userDesc}"

    insult = jasontools.generateChatGPT(chat_prompt)

    return insult   

def get_state():
    return BULLYSTATE

def set_state(state):
    global BULLYSTATE
    if state == True:
        BULLYSTATE = True
    else:
        BULLYSTATE = False

def get_tolerance():
    return BULLYTOLERANCE

def set_tolerance(level):
    global BULLYTOLERANCE
    BULLYTOLERANCE = level

async def checkTarget(update,context):

    message_type: str = update.message.chat.type

    if message_type != "private":
        return None

    userid = update.message.chat.id

    username = update.message.from_user.username

    if updateUser(username,userid):
        return True
    else:
        return False

async def bullytarget(update,context):
    ranNum = random.randint(-1, BULLYTOLERANCE)

    if ranNum != 1:
        return None
    else:
        username: str = update.message.chat.username

        getInsult(username)        

async def bullystatus(update,context):
    bullystate = BULLYSTATE

    if bullystate == True:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Bully Mode Enabled.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Bully Mode Disabled.")

async def bullyenable(update,context):
    set_state(True)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Activating Bully Mode...")

async def bullydisable(update,context):
    set_state(False)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Deactivating Bully Mode...")

async def get_bullytolerance(update, context):
    tolerance = BULLYTOLERANCE

    await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Bully Tolerance Levels: {tolerance}")

async def set_bullytolerance(update, context):
    if context.args: 
        level = context.args[0]

        if level.isdigit():
            level = int(level)
            if level >= 0:
                set_tolerance(level)
                await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Bully Tolerance Set to {level}.")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Minimum Level is 0.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Enter a digit please you fool.")
    else:
        set_tolerance(5)
        await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Bully Tolerance Set to {5}.")


if __name__ == "__main__":
    getInsult("Markryann")