#5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI
#5907729715

import telegram
from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import *

token = '5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI'

LOCATION_BUTTON, LANGUATE_BUTTON = range(2)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)

    return menu

def location_btn(update:Update, context:CallbackContext) -> None:
    user_id = update.effective_chat.id
    btn_list = []
    btn_list.append(InlineKeyboardButton("대전광역시", callback_data="대전광역시"))
    btn_list.append(InlineKeyboardButton("충북", callback_data="충북"))

    show_markup = InlineKeyboardMarkup(build_menu(btn_list, len(btn_list)))
    update.message.reply_text("선택", reply_markup = show_markup)

    return LOCATION_BUTTON

def language_btn(update:Update, context:CallbackContext) -> None:
    query = update.callback_query.data
  
    btn_list = []
    btn_list.append(InlineKeyboardButton("영어", callback_data="영어"))
    btn_list.append(InlineKeyboardButton("일본어", callback_data="일본어"))
    btn_list.append(InlineKeyboardButton("중국어", callback_data="중국어"))

    show_markup = InlineKeyboardMarkup(build_menu(btn_list, len(btn_list)))
    context.bot.send_message(chat_id=update.effective_chat.id, text='선택', reply_markup=show_markup)

    return LANGUATE_BUTTON

updater = Updater(token)

main_handler = ConversationHandler(
            entry_points = [CommandHandler('start',location_btn)],
            states = {
                LOCATION_BUTTON : [CallbackQueryHandler(language_btn)],
                
                #LANGUATE_BUTTON : [CallbackQueryHandler(language_btn)],
            },
            fallbacks = [CommandHandler('cancel',language_btn)],

            map_to_parent={
                ConversationHandler.END:ConversationHandler.END
            }
        )

updater.dispatcher.add_handler(main_handler)
updater.start_polling()
updater.idle()




