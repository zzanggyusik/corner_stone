#5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI
#5907729715

import telegram
from telegram import *
from telegram.ext import Updater, CommandHandler
from telegram.ext import *
from config import *

class Cornerstone:
    def __init__(self) -> None:
        self.user_id = '0'
        self.ENTRY_POINT = 1
        self.LOCATION_BUTTON = 2
        self.LANGUAGE_BUTTON = 3
        self.CANCEL = 4

        self.mainHandler = ConversationHandler(
                entry_points = [CommandHandler('start', self.locationButtonHandler)],
                states = {
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageButtonHandler)],
                },
                fallbacks = [CommandHandler('cancel',self.fallbackHandler)],
                map_to_parent={
                    ConversationHandler.END:ConversationHandler.END
                }
            )

    def introduction(self, update:Update):
            update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다.')
            return self.ENTRY_POINT

    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def locationButtonHandler(self, update:Update, context:CallbackContext) -> None:
        self.introduction(update=update)
        self.user_id = update.effective_chat.id
        print(self.user_id)
        btn_list = []
        btn_list.append(InlineKeyboardButton("대전광역시", callback_data="대전광역시"))
        btn_list.append(InlineKeyboardButton("충청북도", callback_data="충청북도"))

        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))
        context.bot.send_message(chat_id=self.user_id, 
            text='거주하시는 지역을 선택해 주세요.', 
            reply_markup=show_markup
            )

        return self.LOCATION_BUTTON

    def languageButtonHandler(self, update:Update, context:CallbackContext) -> None:
        query = update.callback_query.data
        print(query)

        btn_list = []
        btn_list.append(InlineKeyboardButton("영어", callback_data="영어"))
        btn_list.append(InlineKeyboardButton("일본어", callback_data="일본어"))
        btn_list.append(InlineKeyboardButton("중국어", callback_data="중국어"))

        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))
        context.bot.send_message(chat_id=self.user_id, 
            text='사용하실 언어를 선택해 주세요.', 
            reply_markup=show_markup
            )

        return self.LANGUAGE_BUTTON
    
    def fallbackHandler(self, update:Update, context:CallbackContext):
        update.message.reply_text('이용해 주셔서 감사합니다.')
        return self.CANCEL

bot = Cornerstone()
updater = Updater(token)
updater.dispatcher.add_handler(bot.mainHandler)
updater.start_polling()
updater.idle()




