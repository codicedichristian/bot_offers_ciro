#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import telegram
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler)
import validators
from amazon_bot.mongoConnector import MongoConnector

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

message = {
    'link': '', 
    'amazonLink': '',
    'title': '', 
    'price': '',
    'invecedi': '', 
    'imagelink': ''
} 

item_to_send_list = [] 

messages_to_send_in_another_chann = []


GET_LIST, SEND_MESSAGES, CHOOSING = range(3)

def start(update, context):
    print("mi hanno scritto")
    reply_keyboard = [['Get Messages']]
    update.message.reply_text(
        'Hi, tell me what you want to do!',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHOOSING

def action_switcher(update, context):
    text = update.message.text
    if text == 'Get Messages':
        reply_keyboard = [['Message 1', 'Message 2', 'Message 3']]
        update.message.reply_text(
        'which message?!',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return GET_LIST

def get_list(update, context): 
    mongoConn  = MongoConnector()
    newDiffToMap = mongoConn.getLastItems('ITEMS_DIFF')  
    send_messages(update, context, newDiffToMap)

    
def send_messages(update, context, item_to_send):
    chat_id = update.message.chat_id
    print(chat_id)
    element = []
    i = 0

    for el in item_to_send: 
        text = (f"""
  
💰<b>OFFERTA BEST PRODUCTS</b>
⚡️<b>{el['title']} </b>

<b>🔥 Prezzo Scontato: </b>{el['price']}

👉 <a style="color:blue;">{el['affiliateLink']}</a>

""")
        #url_amazon = 'https://www.amazon.it/ref=as_li_ss_tl?ie=UTF8&linkCode=ll2&tag=techdiscoun09-21&linkId=8928f8f9c6518b80a10fa5e7b70089f8&language=it_IT'
        url_amazon = el['affiliateLink']
        keyboard = [
            [InlineKeyboardButton(" 📲 Apri subito nell'app 🛒", url = url_amazon)], 
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.sendPhoto(chat_id, el['imglink'], text, parse_mode = 'HTML',
        disable_web_page_preview = False, disable_notification = False, reply_markup = reply_markup)
        
        new_element = {
            'chat_id' : chat_id,
            'image_link' : el['imglink'],
            'text' : text,
            'parse_mode' : 'HTML',
            'reply_markup' : reply_markup,
        }
    
        messages_to_send_in_another_chann.append(new_element)

        print("hola estoy aqui")

        keyboardConfirm = [
            [InlineKeyboardButton(" ✅ Invia nel canale ", callback_data = "ok:"+ str(i))], 
        ]
        reply_markup = InlineKeyboardMarkup(keyboardConfirm)
        context.bot.sendMessage(chat_id, "se il messaggio va bene invialo nel canale", reply_markup = reply_markup)
        i = i + 1 
    # DONE 
    return ConversationHandler.END

def button(update, context):
    query = update.callback_query   
    status = query.data.split(":")[0]
    idx = query.data.split(":")[1]
    
    query.answer()
    if status == 'ok':
        element = messages_to_send_in_another_chann[int(idx)]
        channel_nick = '@amazontechdeals2020' # this is for a public channel
        channel_id = '-1001269605441'         # this is for a private channel 
        context.bot.sendPhoto(channel_id, element['image_link'], element['text'], parse_mode = element['parse_mode'],
        disable_web_page_preview = False, disable_notification = False, reply_markup = element['reply_markup'])

        query.edit_message_text(text="Inviato babe! (forse)".format(query.data))
    

def done(update, context):
    print("done")


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='1103532888:AAHToQgHOryMw1JPepltD07QIGC5hy_A3UI', use_context=True)
        
    # handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Get Messages)$'), get_list)],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    # add things to dispatcher
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
    
    
