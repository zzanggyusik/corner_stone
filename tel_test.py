#python-telegram-bot==13.15
#python==3.8.9

#동작 실행 
###check

from config import *
import telegram
from telegram import *
from telegram.ext import *

updater = Updater(token = TOKEN, use_context = True)


handler = ConversationHandler(
    entry_points = [CommandHandler('start',location_select)],
    state = {



    },
    fallbacks = [CommandHandler('cancel',cancel)]
)



def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def cor_location(update, context:CallbackContext):

    show_list = []
    show_list.append(InlineKeyboardButton("충북", callback_data="1")) # add on button
    show_list.append(InlineKeyboardButton("대전", callback_data="2")) # add off button
    show_list.append(InlineKeyboardButton("cancel", callback_data="0")) # add cancel button
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup

    show_markup = InlineDeyboardMarkup(build_menu(btn_list, 3))

    update.message.reply_text("선택 되었습니다",reply_markup = show_markup)

    return LOCATION

def cor_mid(update, context:CallbackContext):

    if query == "1":
        return cor_language(update, context)
    elif query == "2":
        return cor_language(update, context)

def cor_language(update, context:CallbackContext):

    

get_handler = CommandHandler('get', get_command)
updater.dispatcher.add_handler(get_handler)

updater.start_polling(timeout=1, clean=True)
updater.idle()