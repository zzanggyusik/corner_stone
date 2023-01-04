#python-telegram-bot==13.15
#python==3.8.9

#동작 실행 
###check

from config import *
import telegram
from telegram import *
from telegram.ext import *

updater = Updater(token = TOKEN, use_context = True)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def get_command(update, context):
    print("get")
    show_list = []
    show_list.append(InlineKeyboardButton("충북", callback_data="on")) # add on button
    show_list.append(InlineKeyboardButton("대전", callback_data="off")) # add off button
    show_list.append(InlineKeyboardButton("cancel", callback_data="cancel")) # add cancel button
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup

    update.message.reply_text("원하는 값을 선택하세요", reply_markup=show_markup)

get_handler = CommandHandler('get', get_command)
updater.dispatcher.add_handler(get_handler)

updater.start_polling(timeout=1, clean=True)
updater.idle()