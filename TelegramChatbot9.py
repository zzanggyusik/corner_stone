import telegram
from telegram import *
from telegram.ext import CommandHandler
from telegram.ext import *
from ChatbotDB2 import *
import prettytable as pt

TOKEN = '5620332585:AAE6riueZPkYVu3y_v3z5rg3ozaK68ys-Ho'

class CornerstoneChatbot:
    def __init__(self) -> None:
        #============= Updater, Bot ============#
        self.updater = Updater(TOKEN)
        self.sendingBot = telegram.Bot(TOKEN)
        #================== DB =================#
        self.chatbot_db = ChatbotDB()
        #============== User Data ==============#
        self.user_id = ''           # 사용자의 ID, self.locationHandler에서 값이 저장 됨
        self.location = ''          # 선택한 지역, self.languageHandler에서 값이 저장 됨
        self.language = ''          # 선택한 언어, self.messageHandler에서 값이 저장 됨
        #=========== Simulation Data ===========#
        self.post_num = ''
        #============ Return const =============#
        self.LOCATION_BUTTON = 1    
        self.LANGUAGE_BUTTON = 2
        self.DELETE_BUTTON = 3
        #=============== Contant ===============#
        self.isAlready = False
        #================ Main =================#
    
        self.mainHandler = ConversationHandler(
                entry_points = [
                    CommandHandler('start', self.locationHandler)
                ],

                states = {
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageHandler)],
                    self.LANGUAGE_BUTTON : [CallbackQueryHandler(self.messageHandler)],
                },

                fallbacks = [
                    CommandHandler('cancel',self.fallbackHandler),
                    CommandHandler('option', self.languageHandler),
                    CommandHandler('start', self.locationHandler),
                    CommandHandler('delete', self.deleteButtonHandler)
                ],

                map_to_parent = {
                    ConversationHandler.END:ConversationHandler.END
                }
            )
    #=============== Method ==================#
   
    def introduction(self, update:Update):
            update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다. 🙂')
  
    def showHint(self, update:Update):
            table = pt.PrettyTable(['function', 'enter'])
            table.align['function'] = 'm'
            table.align['enter'] = 'm'

            #수정 : 이름 변경
            data = [
                ('start','/start '),
                ('reset','/cancel'),
                ('language_append','/option'),
                ('language_delete','/delete')                
            ]
            for start, language_append in data:
                table.add_row([start, language_append])

            update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)

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

    def sendMessageWithSim(self):
        if(self.isAlready == False):
            if(self.chatbot_db.visited_user(self.chatbot_db.con, self.user_id)):
                self.isAlready = True
        if self.isAlready == True:
            print(self.language)
            for lang in self.language:  ##self.language가 리스트 형태
                message = self.chatbot_db.search_data(
                    self.chatbot_db.con, 
                    lang, 
                    self.location,
                    self.post_num,
                    mode = 1
                )

                # 긴급 재난 문자 전송
                for i in range(0, len(message)):
                    str_message = str(message[i])
                    self.sendingBot.send_message(
                        chat_id=self.user_id,
                        text = str_message
                    )

    def mySendMessage(self, update:Update, context:CallbackContext):
        print(self.language)
        print(self.location)
        for lang in self.language: ##self.language가 리스트 형태
            message = self.chatbot_db.search_data(
                self.chatbot_db.con, 
                lang, 
                self.location,
                self.post_num,
                mode = 0
            )

        # 긴급 재난 문자 전송
            for i in range(0, len(message)):
                str_message = str(message[i])
                context.bot.send_message(
                    chat_id=self.user_id,
                    text = str_message
                )
    #=========== Callback Method(Handler) ==============#
    def locationHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id

        self.chatbot_db.con = self.chatbot_db.connection()
        self.language = self.chatbot_db.user_language(self.chatbot_db.con, self.user_id)
        self.location = self.chatbot_db.user_location(self.chatbot_db.con, self.user_id)
        if  self.chatbot_db.visited_user( 
            #수정 db반환값 user_con -> con 변경
            self.chatbot_db.con,
            self.user_id
        ) == True:
            self.mySendMessage(update=update, context=context)
            return self.LANGUAGE_BUTTON

        self.introduction(update)
        self.showHint(update)
        
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
        self.user_id = update.effective_chat.id
        if update.callback_query != None:
            print('init self.location!')
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
        self.user_id = update.effective_chat.id
        if update.callback_query != None:
            print('init self.language')
            self.language = update.callback_query.data

        print(self.language)

        self.chatbot_db.dbHandler(
            self.user_id, 
            self.language, 
            self.location
        )   
        self.language = self.chatbot_db.user_language(self.chatbot_db.con, self.user_id)
        self.mySendMessage(update=update, context=context)

        self.isAlready = True
        # return ConversationHandler.END
    
    #수정 : reset으로 바꾸기
    def fallbackHandler(self, update:Update, context:CallbackContext):
        self.user_id = updatd.effective_chat.id
    
        self.chatbot_db.remove_id(
            self.chatbot_db.con,
            self.user_id,
        )

        update.message.reply_text('이용해 주셔서 감사합니다.')

    def deleteButtonHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id

        btnText_list = [
            '영어', '일본어', '중국어'
        ]

        context.bot.send_message(
            chat_id=self.user_id, 
            text = '🌎삭제하실 언어를 선택해 주세요.', 
            reply_markup = self.createButton(btnText_list)
        )
        
        return self.DELETE_BUTTON

    def deleteLangHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id

        if update.callback_query != None:
            self.language = update.callback_query.data

        self.chatbot_db.remove_data(
            self.chatbot_db.con,
            self.user_id,
            self.language
        )

        context.bot.send_message(
                chat_id=self.user_id,
                text = self.language + '가 삭제되었습니다.🙂'
        )
        return self.LANGUAGE_BUTTON