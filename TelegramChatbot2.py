import telegram
from telegram import *
from telegram.ext import Updater, CommandHandler
from telegram.ext import *
from config import *

import prettytable as pt

class Cornerstone:
    def __init__(self) -> None:
        #============== User Data ==============#
        self.user_id = ''           # 사용자의 ID, self.locationButtonHandler에서 값이 저장 됨
        self.location = ''          # 선택한 지역, self.languageButtonHandler에서 값이 저장 됨
        self.language = ''          # 선택한 언어, self.sendMessageHandler에서 값이 저장 됨
        #============ Return const =============#
        self.ENTRY_POINT = 1
        self.LOCATION_BUTTON = 2    
        self.LANGUAGE_BUTTON = 3
        self.SAVE_DATA = 4
        self.CANCEL = 5
        #=======================================#
        self.mainHandler = ConversationHandler(
                entry_points = [CommandHandler('start', self.locationButtonHandler)],
                states = {
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageButtonHandler)],
                    self.LANGUAGE_BUTTON : [CallbackQueryHandler(self.sendMessageHandler)]
                },
                fallbacks = [CommandHandler('cancel',self.fallbackHandler)],
                map_to_parent={
                    ConversationHandler.END:ConversationHandler.END
                }
            )

    def introduction(self, update:Update):
            update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다.')

            table = pt.PrettyTable(['function', 'input'])
            table.align['function'] = 'l'
            table.align['input'] = 'l'
            # table.align['Change'] = 'r'

            data = [
                ('start','\start '),
                ('option','\option'),
            ]
            for start, option in data:
                table.add_row([start, option])

            update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)

            return self.ENTRY_POINT

    # DB 데이터 관리
    def dbHandler(self) -> None:
        # User ID : self.user_id
        # Location : self.location
        # Language : self.language
        return True

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
        btn_list = []
        btn_list.append(InlineKeyboardButton("대전광역시", callback_data="대전광역시"))
        btn_list.append(InlineKeyboardButton("충북", callback_data="충북"))

        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))
        context.bot.send_message(chat_id=self.user_id, 
            text='거주하는 지역을 선택해 주세요.', 
            reply_markup=show_markup
        )
        return self.LOCATION_BUTTON

    def languageButtonHandler(self, update:Update, context:CallbackContext) -> None:
        self.location = update.callback_query.data
        print(self.location)

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

    def sendMessageHandler(self, update:Update, context:CallbackContext) -> None:
        self.language = update.callback_query.data
        print(self.language)
        self.dbHandler()

        message = '긴급 재난 문자'

        # 긴급 재난 문자 전송
        context.bot.send_message(chat_id=self.user_id,
            text=message
        )
        return self.SAVE_DATA
    
    def fallbackHandler(self, update:Update, context:CallbackContext):
        update.message.reply_text('이용해 주셔서 감사합니다.')
        return self.CANCEL

bot = Cornerstone()
updater = Updater(TOKEN)
updater.dispatcher.add_handler(bot.mainHandler)
updater.start_polling()
updater.idle()