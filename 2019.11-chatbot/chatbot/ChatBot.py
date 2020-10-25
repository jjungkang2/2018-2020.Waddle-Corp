import sys
import ChatBotModel
import requests
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
import json
import threading
import time

### make button
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def check_order2(id):
    try:
        set_menu = []
        set_menu.append(InlineKeyboardButton("응 내가 할게", callback_data="yes")) 
        set_menu.append(InlineKeyboardButton("지금 바빠", callback_data="no"))
        set_menu_markup = InlineKeyboardMarkup(build_menu(set_menu, len(set_menu) - 1)) 

        waddle.sendMessage(id, "결제 요청이 들어왔습니다.\n맡아 결제 하시겠습니까?", reply_markup=set_menu_markup)
    
    except:
        print("error from check_order")

def check_order(bot, args):
    check_order2(bot.message.chat.id)
    
def manager_order(id):
    try:
        comment = "주문 정보는 다음과 같습니다.\n어쩌구저쩌구.."
        waddle.sendMessage(id, comment)

    except:
        print("error from manager_order")

def complete_order(id, reply_text, text):
    try:
        comment = "'" + reply_text + "'의 답장은 '" + text + "'입니다."        
        waddle.sendMessage(id, comment)

    except:
        print("error from complete_order")
    

### button clicked
def callback_get(bot, update):
    if bot.callback_query.data=="yes":
        manager_order(bot.callback_query.message.chat.id)
    elif bot.callback_query.data=="no": 
        waddle.sendMessage(bot.callback_query.message.chat.id, "다음 기회에..")

### text came
def text(bot, update):
    print(bot.message)
    if bot.message.reply_to_message is not None:
        complete_order(bot.message.chat.id, bot.message.reply_to_message.text, bot.message.text)
    else:
        waddle.sendMessage(bot.message.chat.id, "환영합니다")

### print log
def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


if __name__ == '__main__':

    waddle = ChatBotModel.WaddleBot()
    waddle.add_handler('order', check_order)
    waddle.add_query_handler(callback_get)
    waddle.add_message_handler(text)
    waddle.add_error_handler(error)
    waddle.start()