#python-telegram-bot==13
#python==3.8.9

#동작 실행 확인

import telegram
from telegram import *
from telegram.ext import *

TOKEN = "5620332585:AAE6riueZPkYVu3y_v3z5rg3ozaK68ys-Ho"
#ID = '5508231825' #id 불러오기 필요

updater = Updater(token = TOKEN, use_context = True)

# def first_button(update, context):
#     task_button = [
#         InlineKeyboardButton('유성구 덕명동', callack_data=1)
#         , InlineKeyboardButton('유성구 관평동', callbak_data=2)
#     ]

#     reply_markup = InlineKeyboardMarkup(task_button)

#     context.bot.send_message(
#         chat_id=update.message.chat_id
#         , text='작업을 선택해주세요.'
#         , reply_markup=reply_markup
#     )
# task_buttons_handler = CommandHandler('cornerstone', first_button)

# dispatcher.add_handler(task_buttons_handler)

# updater.start_polling()
# updater.idle()

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
    show_list.append(InlineKeyboardButton("유성구 덕명동", callback_data="on")) # add on button
    show_list.append(InlineKeyboardButton("유성구 관평동", callback_data="off")) # add off button
    show_list.append(InlineKeyboardButton("cancel", callback_data="cancel")) # add cancel button
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup

    update.message.reply_text("원하는 값을 선택하세요", reply_markup=show_markup)

get_handler = CommandHandler('get', get_command)
updater.dispatcher.add_handler(get_handler)

updater.start_polling(timeout=1, clean=True)
updater.idle()