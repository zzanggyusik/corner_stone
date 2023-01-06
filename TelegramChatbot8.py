import telegram
from telegram import *
from telegram.ext import CommandHandler, Filters
from telegram.ext import *
from ChatbotDB import *
import prettytable as pt
import config

class CornerstoneChatbot:
    def __init__(self) -> None:
        #============= Updater, Bot ============#
        self.updater = Updater(config.TOKEN)
        self.sendingBot = telegram.Bot(config.TOKEN)
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
        #ConversationHandler를 통한 흐름 제어
        self.mainHandler = ConversationHandler(
                #이벤트에 대한 CommandHandler생성(command[명령어], callback[응답])
                #entry_points : 가장 먼저 실행되는 Handler
                entry_points = [
                    CommandHandler('start', self.locationHandler)
                ],
                #states : return const에 따라 호출되는 Handler
                states = {
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageHandler)],
                    self.LANGUAGE_BUTTON : [CallbackQueryHandler(self.messageHandler)],
                    self.DELETE_BUTTON : [CallbackQueryHandler(self.deletedbHandler)]
                },
                #falbacks : 순서 무관, 조건 만족 시 Handler
                fallbacks = [
                    CommandHandler('cancel',self.fallbackHandler),
                    CommandHandler('option', self.languageHandler),
                    CommandHandler('start', self.locationHandler),
                    CommandHandler('delete', self.deleteHandler)
                ],

                map_to_parent = {
                    ConversationHandler.END:ConversationHandler.END
                }
            )
    #=============== Method ==================#
    def introduction(self, update:Update):
        '''시작 메시지 출력, 
            self.locationHandler함수에서 호출 '''

        update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다. 🙂')
   
    def showHint(self, update:Update):
        '''시작 메시지 후 챗봇 사용법 테이블 출력, 
            self.loacationHandler함수에서 호출'''

        table = pt.PrettyTable(['function', 'enter'])
        table.align['function'] = 'm'
        table.align['input'] = 'm'

        data = [
            ('start','/start '),
            ('option','/option'),
            #[23.1.6.14:26]수정 : 추가
            ('delete','/delete'),
            ('cancel','/cancel')
        ]
        for start, option in data:
            table.add_row([start, option])

        update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)

    #버튼 생성
    #self.locationHandler, self.languageHandler, self.deleteHandler 에서 InlineKeyboardMarkup 함수 인자로 사용
    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        '''버튼 메뉴 생성 함수'''
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def createButton(self, btnText_list):
        '''버튼 생성 함수'''
        btn_list = []

        for text in btnText_list:
            btn_list.append(InlineKeyboardButton(text, callback_data=text))

        #show_markup : btn_list로 만들어진 버튼 메뉴 담김
        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))
        return show_markup

    #새로운 봇 생성으로 메시지 전달
    def sendMessageWithSim(self):
        '''시뮬레이션에서 정보 갱신될 때, 메시지 전송'''
        #isAlready ?
        #데이터가 모두 존재하면 isAlready
        if self.isAlready == True:
            message = self.chatbot_db.search_data(
                self.chatbot_db.message_con, 
                self.language, 
                self.location,
                #최신 데이터 1개 뽑기
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

    #start_polling
    def mySendMessage(self, update:Update, context:CallbackContext):
        message = self.chatbot_db.search_data(
            self.chatbot_db.message_con, 
            self.language, 
            self.location,
            #최신 데이터 1개 뽑기
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
        '''지역 버튼'''
        #현재 user의 id 가져옴
        self.user_id = update.effective_chat.id

        self.chatbot_db.conDB()
        if  self.chatbot_db.visited_user(
            self.chatbot_db.user_con,
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
        '''언어 버튼'''
        self.user_id = update.effective_chat.id

        #값이 있으면 지역 값 선택 된걸로
        if update.callback_query != None:
            print('init self.location!')
            self.location = update.callback_query.data
        print(self.location)

        #버튼 선택
        btnText_list = [
            '영어', '일본어', '중국어'
        ]

        context.bot.send_message(
            chat_id=self.user_id, 
            text = '🌎사용할 언어를 선택해 주세요.', 
            reply_markup = self.createButton(btnText_list)
        )
        return self.LANGUAGE_BUTTON

    def deleteHandler(self, update:Update, context: CallbackContext):
        '''언어 삭제'''
        self.user_id = update.effective_chat.id

        if update.callback_query != None:
            self.location = update.callback_query.data

        btnText_list = [
            '영어', '일본어', '중국어'
        ]
            
        context.bot.send_message(
            chat_id=self.user_id, 
            text = '🌎삭제할 언어를 선택해 주세요.', 
            reply_markup = self.createButton(btnText_list)
        )
        return self.DELETE_BUTTON

    def messageHandler(self, update:Update, context:CallbackContext):
        '''db내용 저장'''
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

        self.mySendMessage(update=update, context=context)
        self.isAlready = True

    def deletedbHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id

        if update.callback_query != None:
            self.language = update.callback_query.data

        self.chatbot_db.remove_data(
            self.chatbot_db.user_con,
            self.user_id,
            self.language
        )
    
    #fallback 인자에 들어간 Handler에서 호출하는 callback함수
    def fallbackHandler(self, update:Update, context:CallbackContext):
        '''종료시 출력'''
        update.message.reply_text('이용해 주셔서 감사합니다.')
