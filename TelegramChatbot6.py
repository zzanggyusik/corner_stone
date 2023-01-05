from telegram import *
from telegram.ext import CommandHandler
from telegram.ext import *
import prettytable as pt
from sqlite3 import Error
import sqlite3

TOKEN = "5620332585:AAE6riueZPkYVu3y_v3z5rg3ozaK68ys-Ho"

class CornerstoneChatbot:
    def __init__(self, update_token) -> None:

        self.updater = Updater(update_token)
        self.dispatcher = self.updater.dispatcher

        self.engine = 

        
        
        #============== User Data ==============#
        self.user_id = ''           # 사용자의 ID, self.locationHandler에서 값이 저장 됨
        self.location = ''          # 선택한 지역, self.languageHandler에서 값이 저장 됨
        self.language = ''          # 선택한 언어, self.messageHandler에서 값이 저장 됨
        #============ Return const =============#
        self.LOCATION_BUTTON = 1    
        self.LANGUAGE_BUTTON = 2
        #================ Main =================#
        self.mainHandler = ConversationHandler(
                entry_points = [
                    CommandHandler('start', self.locationHandler)
                ],

                states = {
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageHandler)],
                    self.LANGUAGE_BUTTON : [CallbackQueryHandler(self.messageHandler)]
                },

                fallbacks = [
                    CommandHandler('cancel',self.fallbackHandler),
                    CommandHandler('start',self.locationHandler),
                    CommandHandler('option', self.languageHandler),
                    CommandHandler('message',self.messageHandler2)
                ],

                map_to_parent = {
                    ConversationHandler.END:ConversationHandler.END
                }
            )
    #============ Handler, Method ==============#
    def introduction(self, update:Update):
            update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다. 🙂')

            table = pt.PrettyTable(['function', 'enter'])
            table.align['function'] = 'm'
            table.align['input'] = 'm'

            data = [
                ('start','/start '),
                ('option','/option'),
            ]
            for start, option in data:
                table.add_row([start, option])

            update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)

    def dbHandler(self)->None:
        # User ID : self.user_id
        # Location : self.location
        # Language : self.language
        # user_info = []                  
        # user_info.extend([id, language, region])
        # self.insert_table(self.user_con, user_info[0], user_info[1], user_info[2])

        return True

    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def createButton(self, btnText_list):
        btn_list = []

        for text in btnText_list:
            btn_list.append(InlineKeyboardButton(text, callback_data=text))

        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))
        return show_markup

    def locationHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id
        self.introduction(update)
        # self.showHint(update)
       
        btnText_list = [
            '대전광역시', '충청북도'
        ]

        context.bot.send_message(
            chat_id=self.user_id, 
            text = '🧭거주하는 지역을 선택해 주세요.', 
            reply_markup = self.createButton(btnText_list)
        )
        return self.LOCATION_BUTTON

    def languageHandler(self, update:Update, context:CallbackContext):
        if self.location == '':
            self.location = update.callback_query.data
        print(self.location)

        btnText_list = [
            '영어', '일본어', '중국어'
        ]

        context.bot.send_message(
            chat_id=self.user_id, 
            text = '🌎사용하실 언어를 선택해 주세요.', 
            reply_markup = self.createButton(btnText_list)
        )
        return self.LANGUAGE_BUTTON

    def messageHandler(self, update:Update, context:CallbackContext):
        self.language = update.callback_query.data
        print(self.language)
        self.dbHandler()

        context.bot.send_message(chat_id = self.user_id,
            text="/message를 입력해주세요"
        )
        
    def messageHandler2(self, update:Update, context:CallbackContext):

        message = '긴급 재난 문자'
        context.bot.send_message(chat_id = self.user_id,
            text=message
        )

        # message = '긴급 재난 문자'
        # # 긴급 재난 문자 전송
        # # for i in range(0, len(message)):
        # #     str_message = str(message[i])
        # #     context.bot.send_message(chat_id=self.user_id,
        # #         text = str_message
        # #     )
        # context.bot.send_message(chat_id=self.user_id,
        #     text=message
        # )

    def fallbackHandler(self, update:Update, context:CallbackContext):
        update.message.reply_text('이용해 주셔서 감사합니다.')

