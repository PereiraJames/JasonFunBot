import os
import json
from bully import bully, targetting
import jasontools
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import random
import sys
from datetime import datetime
import re

BOT_TOKEN = jasontools.parseEnvFile("BOT_TOKEN")
BOT_USERNAME = jasontools.parseEnvFile("BOT_USERNAME")

MASTER_USERNAME = jasontools.parseEnvFile("TELE_MASTERNAME")
MASTER_ID = jasontools.parseEnvFile("TELE_MASTERID")
HERMES_ID = jasontools.parseEnvFile("TELE_HERMESID")
TELE_DRANKSID = jasontools.parseEnvFile("TELE_DRANKSID")

userstates = {}

async def helpPeon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # logAttempts("/help",update)

    commands = jasontools.readCommandList()

    print(commands)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=commands)

async def alertMaster(update: Update, context: ContextTypes.DEFAULT_TYPE, alertMessage):

    message_type: str = update.message.chat.type

    username: str = update.message.from_user.username

    if message_type != "private":
        message_type = update.message.chat.title                 

    alert = f"ALERT: {username} ({message_type}) | {alertMessage}"

    print(alert)
    await context.bot.send_message(chat_id=HERMES_ID,text=alert)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username: str = update.message.chat.username

    message_type: str = update.message.chat.type

    userid = update.message.chat.id

    if message_type != "private":
        message_type = update.message.chat.title

    text: str = update.message.text

    targetsName = update.message.from_user.username
    incomingmessage = f'{targetsName} ({update.message.chat.id}) in {message_type}: "{text}"'

    print(incomingmessage, message_type)
    messagelog(incomingmessage, message_type, targetsName)

    if str(targetsName) != MASTER_USERNAME:
        messagealert = "Sent: " + "\n" + text

        await alertMaster(update, context, messagealert)

    messagealert = "Sent: " + "\n" + text

    await alertMaster(update, context, messagealert)

    if await bully.checkTarget(update,context):
        useralert = f"Added {username} ({userid}) to Jason's Pokédex"

        await alertMaster(update, context, useralert)
        


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Can be used to get user information
    print(f'Update {update} caused error {context.error}')
    await alertMaster(update, context, f'Update {update} caused error {context.error}')
    return

def logAttempts(commandName, update: Update):
    
    user = update.effective_user.username
    
    message_type: str = update.message.chat.type

    if message_type != "private":
        message_type = update.message.chat.title
    
    logAttempt = f"{user} used the {commandName} command."
    
    messagelog(logAttempt, message_type, user)    
    alert = f"{user} used the {commandName} command."
    print(alert)
    return

def messagelog(incoming_message, grouptype, person):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if grouptype == "private":
        filename = f'messagelogs/{grouptype}/{person}.txt'
    else:
        filename = f'messagelogs/{grouptype}/{grouptype}.txt'
    if not os.path.isfile(filename):
        print(f"Creating {filename}")
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'a') as file:
        file.write("(" + current_time + ") " + incoming_message + '\n')

if __name__ == "__main__":
    print("Jason Intializing...")

    app = Application.builder().token(BOT_TOKEN).build()

    # Normal Commands
    app.add_handler(CommandHandler('help', helpPeon))

    # MASTER Commands
    
    #BULLY MODULE
    app.add_handler(CommandHandler('bullystatus', bully.bullystatus, filters.User(username=MASTER_USERNAME)))
    app.add_handler(CommandHandler('bullyenable', bully.bullyenable, filters.User(username=MASTER_USERNAME)))
    app.add_handler(CommandHandler('bullydisable', bully.bullydisable, filters.User(username=MASTER_USERNAME)))
    app.add_handler(CommandHandler('setbullylevel', bully.set_bullytolerance, filters.User(username=MASTER_USERNAME)))
    app.add_handler(CommandHandler('getbullylevel', bully.get_bullytolerance, filters.User(username=MASTER_USERNAME)))





    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error) 

    app.run_polling(poll_interval=1)