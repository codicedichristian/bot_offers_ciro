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

messageToSend = {
    'chat_id':'', 
    'image_link':'', 
    'text': '', 
    'parse_mode': '', 
    'reply_markup':'',
}


CHOOSING, MESSAGE_SWITCH, ASK_IMAGE, IMAGE= range(4)

def start(update, context):
    print("eccolo")
    reply_keyboard = [['Get Messages', 'WIP1', 'WIP2']]
    update.message.reply_text(
        'Hi, tell me what you want to do!',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CHOOSING

def action_switcher(update, context):
    text = update.message.text
    print(update, context)
    if text == 'Get Messages':
        reply_keyboard = [['Message 1', 'Message 2', 'Message 3']]
        update.message.reply_text(
        'which message?!',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return MESSAGE_SWITCH

    elif text == 'WIP1':
        print("ciao")
    else: 
        print("ciao")

def get_messages(update, context): 
    text = update.message.text
    query = update.callback_query
    if text == 'Message 1': 
        update.message.reply_text('give me link, openlink, title, price, invecedi')
        return ASK_IMAGE
    elif text == 'Message 2': 
        print("ciao")
    else: 
        print("ciao")

def check_message(info):
    numPattern = re.compile("^[0-9,.]+$")
    returnVar = True 
    returnVar = (numPattern.match(info[3]) and numPattern.match(info[4]))
    returnVar = validators.url(info[0])
    returnVar = validators.url(info[1])
    return returnVar


def save_body_ask_image(update, context): 
    text = update.message.text
    info = text.split('\n')
    if(check_message(info)):
        message['link'] = info[0]
        message['amazonLink'] = info[1]
        message['title'] = info[2]
        message['price'] = info[3].replace(',','.')
        message['invecedi'] = info[4].replace(',','.')
        message['delta'] = ((float(message['invecedi']) - float(message['price']) / float(message['invecedi'])) * 100)
        update.message.reply_text('great, now the image')
        return IMAGE
    else: 
        update.message.reply_text('sorry, retry it')
        return ASK_IMAGE
   

def save_image(update, context): 
    image_id = update.message.photo[-1].file_id
    message['image'] = image_id
    send_message(update, context)

def send_message(update, context):
    chat_id = update.message.chat_id
    text = f""" 
  
💰<b>OFFERTA BEST PRODUCTS</b>
⚡️<b>{message['title']} </b>

<b>💲 Prezzo Scontato: </b>{message['price']} €
❌ Invece di: {message['invecedi']} €
🔥 Risparmi: {message['delta']} % 

👉 <a style="color:blue;">{message['link']}</a>

"""
    #url_amazon = 'https://www.amazon.it/ref=as_li_ss_tl?ie=UTF8&linkCode=ll2&tag=techdiscoun09-21&linkId=8928f8f9c6518b80a10fa5e7b70089f8&language=it_IT'
    url_amazon = message['amazonLink']
    keyboard = [
        [InlineKeyboardButton(" 📲 Apri subito nell'app 🛒", url = url_amazon)], 
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.sendPhoto(chat_id, message['image'], text, parse_mode = 'HTML',
    disable_web_page_preview = False, disable_notification = False, reply_markup = reply_markup)
    
    messageToSend['chat_id'] = chat_id
    messageToSend['image_link'] = message['image']
    messageToSend['text'] = text
    messageToSend['parse_mode'] = 'HTML'
    messageToSend['reply_markup'] = reply_markup

    keyboardConfirm = [
        [InlineKeyboardButton(" ✅ Invia nel canale ", callback_data = 'ok')], 
    ]
    reply_markup = InlineKeyboardMarkup(keyboardConfirm)
    context.bot.sendMessage(chat_id, "se il messaggio va bene invialo nel canale", reply_markup = reply_markup)
    
    # DONE 
    return ConversationHandler.END

def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'ok':
        context.bot.sendPhoto('@amazontechdeals', messageToSend['image_link'], messageToSend['text'], parse_mode = messageToSend['parse_mode'],
        disable_web_page_preview = False, disable_notification = False, reply_markup = messageToSend['reply_markup'])

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
    updater = Updater(token='1082786262:AAHUOgbsO1k7ybuCr3N1X_5WLWyW-ZE0WxI', use_context=True)

    # handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^(Get Messages|WIP1|WIP2)$'), action_switcher)],
            MESSAGE_SWITCH: [MessageHandler(Filters.regex('^(Message 1|Message 2|Message 3)$'), get_messages)],
            ASK_IMAGE: [MessageHandler(Filters.text, save_body_ask_image)], 
            IMAGE: [MessageHandler(Filters.photo, save_image)]
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
    
    
