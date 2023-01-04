#5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI
#5907729715

import telegram
from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import *

token = '5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI'
bot = telegram.Bot(token=token)
updates = bot.getUpdates()
#print(updates[0]['message']['chat']['id'])

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)

    return menu

def btnTest(update:Update, context:CallbackContext) -> None:
    btn_list = []
    btn_list.append(InlineKeyboardButton("버튼 1", callback_data="1"))
    btn_list.append(InlineKeyboardButton("버튼 2", callback_data="2"))
    btn_list.append(InlineKeyboardButton("버튼 3", callback_data="3"))

    show_markup = InlineKeyboardMarkup(build_menu(btn_list, len(btn_list)))
    update.message.reply_text("선택", reply_markup = show_markup)

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('hi', btnTest))
updater.start_polling()