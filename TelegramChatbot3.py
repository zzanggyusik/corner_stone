import telegram
from telegram import *
from telegram.ext import Updater, CommandHandler
from telegram.ext import *
from sqlite3 import Error
import sqlite3
from config import *
import prettytable as pt

user_info = []

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
        #================= MAIN ================#
        #ConversationHandler를 통한 Handler흐름제어
        self.mainHandler = ConversationHandler(
                #각 이벤트에 대한 CommandHandler생성(comand[명령어], callback[응답])
                #entry_point : 챗봇 시작, 가장 먼저 실행 Handler
                entry_points = [CommandHandler('start', self.locationButtonHandler)],

                #states : return const에 따라 호출되는 Handler
                states = {
                    #지역 버튼 선택시 언어 버튼 응답
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageButtonHandler)],
                    #언어 버튼 선택시 메시지 응답
                    self.LANGUAGE_BUTTON : [CallbackQueryHandler(self.sendMessageHandler)]
                },

                #cancel, 종료
                #falbacks : 순서 무관, 조건 만족시 Handler
                fallbacks = [CommandHandler('option',self.languageButtonHandler), 
                             CommandHandler('cancel',self.fallbackHandler),
                             CommandHandler('start',self.locationButtonHandler)
                            ], 

                map_to_parent={
                    ConversationHandler.END:ConversationHandler.END
                }
            )
    
    #DB연동
    #시작, 메시지 보내기
    #self.locationButtonHandler callback 함수에서 호출
    def introduction(self, update:Update):
            update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다 🙂')

            #table을 통한 출력
            table = pt.PrettyTable(['function', 'input'])
            table.align['function'] = 'l'
            table.align['input'] = 'l'

            data = [
                ('start','/start '),
                ('language','/language'),
                ('cancel','/cancel')
            ]
            for start, option in data:
                table.add_row([start, option])

            update.message.reply_text(f'<pre>{table}</pre>', parse_mode=ParseMode.HTML)

            return self.ENTRY_POINT

    # DB 데이터 관리
    # self.sendMessageHandler에서 호출
    def dbHandler(self) -> None:
        # User ID : self.user_id
        # Location : self.location
        # Language : self.language
        return True

    #버튼 생성 함수
    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    #callback 함수
    #지역 설정 버튼
    def locationButtonHandler(self, update:Update, context:CallbackContext) -> None:
        #introduction함수호출
        self.introduction(update=update)

        #chat_id가져옴
        self.user_id = update.effective_chat.id

        #button 메뉴
        btn_list = []
        btn_list.append(InlineKeyboardButton("대전광역시", callback_data="대전광역시"))
        btn_list.append(InlineKeyboardButton("충북", callback_data="충북"))

        #btn_list를 기반으로 만들어진 버튼 메뉴가 담기는 변수
        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))

        #메시지 출력
        context.bot.send_message(chat_id=self.user_id, 
            text='🧭 거주하는 지역을 선택해 주세요.', 
            reply_markup=show_markup
        )
        return self.LOCATION_BUTTON

    #callback 함수
    #언어 설정 버튼
    #self.locationButtonHandler을 통해 생성된 버튼(지역)을 누르면 update.callback_query.data에 해당 버튼의 callback_data 저장
    def languageButtonHandler(self, update:Update, context:CallbackContext):
        if self.location == '': 
            self.location = update.callback_query.data
            print(self.location)
            
        btn_list = []
        btn_list.append(InlineKeyboardButton("영어", callback_data="영어"))
        btn_list.append(InlineKeyboardButton("일본어", callback_data="일본어"))
        btn_list.append(InlineKeyboardButton("중국어", callback_data="중국어"))

        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))
        context.bot.send_message(chat_id=self.user_id, 
            text='🌎 사용하실 언어를 c선택해 주세요.', 
            reply_markup=show_markup
            )

        return self.LANGUAGE_BUTTON

    #callback 함수
    #db내용 저장
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
    
    #callback 함수
    #마무리 멘트 : cancel
    def fallbackHandler(self, update:Update, context:CallbackContext):
        update.message.reply_text('이용해 주셔서 감사합니다.')
        return self.CANCEL

bot = Cornerstone()
updater = Updater(TOKEN)
updater.dispatcher.add_handler(bot.mainHandler)
updater.start_polling()
updater.idle()