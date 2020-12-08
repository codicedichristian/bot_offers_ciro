#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


replykbrd = [
    [
        'mangiare',
        'cucina',
        'elettronica',
        'tools'
    ],
    [
        'computer',
        'sports',
        'boost',
        'mix pg1'
    ],
    [
        'mix pg2',
        'mix pg3',
        'mix pg4',
    ],
    [
        'mix pg5',
        'mix pg6',
    ]
]

message = {
    'link': '', 
    'amazonLink': '',
    'title': '', 
    'price': '',
    'invecedi': '', 
    'imagelink': ''
} 

item_to_send_list = [] 

messages_to_send_in_another_chann = {}


GET_LIST, GET_TECH_LIST, SEND_MESSAGES, CREATE_MSG, CHOOSING, ASK_FOR_LINK = range(6)

def start(update, context):
    chat_id = update.message.chat_id
    print(chat_id)
    if(chat_id != 1237137064):
        context.bot.sendMessage(chat_id, "sorry, you're not my boss.")
        return

    print("mi hanno scritto")
    reply_keyboard = replykbrd
    update.message.reply_text(
        'Hi, tell me what you want to do!',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return CHOOSING

def action_switcher(update, context):
    text = update.message.text
    
    if(text == "create msg"):
        return ASK_FOR_LINK
    if(text.lower() == "last"): 
        collection =  "LAST_LAUNCH"
        mongoConn  = MongoConnector()
        items = mongoConn.getAllItems(collection)
        for item in items: 
            send_last_date_message(update, context, item['date'])
        return 
    
    mongoConn  = MongoConnector()
    items_to_send = mongoConn.getLastItems(text, True)  
    send_messages(update, context, items_to_send, text)
    return

def ask_for_link(update, context):
    update.message.reply_text('Hi, give me the link! ;) ')
    return CREATE_MSG

def create_msg(update, context):
    #todo
    return 
# def get_list(update, context): 
#     mongoConn  = MongoConnector()
#     newDiffToMap = mongoConn.getLastItems('ITEMS_DIFF')  
#     send_messages(update, context, newDiffToMap)

def send_last_date_message(update, context, text): 
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id, text)

    return ConversationHandler.END

def send_messages(update, context, item_to_send, textInputMsg = 'default'):
    chat_id = update.message.chat_id
    #this because when you click the green button (invia in un altro canale) it will take the right collection
    messages_to_send_in_another_chann.update({str(textInputMsg): []})
    element = []
    i = 0 
    for el in item_to_send: 
        if(el['inveceDi'] != ""):
            prezzoListino = el['inveceDi'].split(':')[1]
            prezzoPulito = prezzoListino.replace(",",".").replace("€","")
            if("-" in el['price']): 
                scontato = el['price'].split("-")[0] 
            else: 
                scontato = el['price']
            sconto = el['inveceDi'].split(':')[2].replace("(", "").replace(")","").replace("-","")
            title = el['title'].lstrip()
            affiliateLink = el['affiliateLink'] if el['affiliateLink'] else "NO LINK"
            text = (f"""
  
💰<b>OFFERTA BEST PRODUCTS</b>
⚡️<b>{title} </b>

<b>🔥 Prezzo Scontato: </b>{scontato}
<b>❌ Invece Di: </b>{prezzoListino}
<b>📈 Sconto del: </b>{sconto}

👉 <a style="color:blue;">{el['affiliateLink']}</a>

""")    
        else: 
            title = el['title'].lstrip()
            affiliateLink = el['affiliateLink'] if el['affiliateLink'] else "NO LINK"
            text = (f"""
  
💰<b>OFFERTA BEST PRODUCTS</b>
⚡️<b>{title} </b>

<b>🔥 Prezzo Scontato: </b>{el['price']}

👉 <a style="color:blue;">{affiliateLink}</a>

""")    
        #url_amazon = 'https://www.amazon.it/ref=as_li_ss_tl?ie=UTF8&linkCode=ll2&tag=techdiscoun09-21&linkId=8928f8f9c6518b80a10fa5e7b70089f8&language=it_IT'
        if(affiliateLink != "NO LINK"):
            url_amazon = affiliateLink
            keyboard = [
                [InlineKeyboardButton(" 📲 Apri subito nell'app 🛒", url = url_amazon)], 
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
        if(el['imglink'] != ''):
            context.bot.sendPhoto(chat_id, el['imglink'], text, parse_mode = 'HTML',
            disable_web_page_preview = False, disable_notification = False, reply_markup = reply_markup)
        
        new_element = {
            'chat_id' : chat_id,
            'image_link' : el['imglink'],
            'text' : text,
            'parse_mode' : 'HTML',
            'reply_markup' : reply_markup,
        }
            
        tmp_values = messages_to_send_in_another_chann[textInputMsg]
        tmp_values.append(new_element)
        messages_to_send_in_another_chann.update({str(textInputMsg): tmp_values })

        print("sent object from mongo - check it out")

        keyboardConfirm = [
            [InlineKeyboardButton(" ✅ Invia nel canale ", callback_data = "ok:"+ str(i) + ":" + str(textInputMsg))], 
        ]
        reply_markup = InlineKeyboardMarkup(keyboardConfirm)
        context.bot.sendMessage(chat_id, "se il messaggio va bene invialo nel canale", reply_markup = reply_markup)
        i = i+1
    # DONE 
    return ConversationHandler.END

def button(update, context):
    query = update.callback_query   
    status = query.data.split(":")[0]
    idx = query.data.split(":")[1]
    text = query.data.split(":")[2]
    query.answer()
    if status == 'ok':
        element_array = messages_to_send_in_another_chann[text]
        element = element_array[int(idx)]
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
            CHOOSING: [MessageHandler(Filters.regex('^(.*)$'), action_switcher)],
            ASK_FOR_LINK: [MessageHandler(Filters.regex('^(.*)$'), ask_for_link)],
            CREATE_MSG: [MessageHandler(Filters.regex('^(.*)$'), create_msg)],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
    )

    # add things to dispatcher
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    print("started listening")
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
    
    
