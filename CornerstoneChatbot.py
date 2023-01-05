from telegram import *
from telegram.ext import CommandHandler
from telegram.ext import *
import prettytable as pt
from sqlite3 import Error
import sqlite3

class CornerstoneChatbot:
    def __init__(self) -> None:
        #============== User Data ==============#
        self.user_id = ''           # 사용자의 ID, self.locationHandler에서 값이 저장 됨
        self.location = ''          # 선택한 지역, self.languageHandler에서 값이 저장 됨
        self.language = ''          # 선택한 언어, self.messageHandler에서 값이 저장 됨
        #============ Return const =============#
        self.LOCATION_BUTTON = 1    
        self.LANGUAGE_BUTTON = 2
        #================ Main =================#
        '''
        # ConversationHandler를 통해 Handler 흐름 제어
        # CommandHandler(comand, callback) : 특정 입력(comand)이 들어 왔을 경우 callback 함수를 호출 함.
            ex) CommandHandler('start', self.MyFunc) : /start가 입력 되면, self.MyFunc이 호출 됨
        # CallbackQueryHandler(callback) : 다른 Handler에서 Callback이 
            요청되면(update.callback_query.data에 값이 전달 되면) callback 함수를 호출 함.
            issue) CommandHandler의 경우 callback 함수가 종료되도 update.callback_query.data에
                    값을 전달 하지 않아 CallbackQueryHandler가 호출되지 않음
            Hint) CallbackQueryHandler는 버튼이 눌리면, update.callback_query.data에 해당하는 버튼의
                    callback_data가 전달되어 잘 동작함
        # entry_point : 챗봇이 시작 됐을 때, 가장 먼저 실행 되는 Handler
        # state : Return const에 따라 호출하는 Handler 결정
        # fallbacks : 순서에 상관없이 특정 조건이 만족하면 Handler 결정
            ex) CommandHandler를 전달 하면, 순서에 상관 없이 comand가 입력 됐을 때, callback 함수가 호출 됨
            Hint) 여러개의 Handler를 전달 할 수 있음
        # map_to_parent : 정확히 모르겠음, 없으면 오류 남
        '''
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
                    CommandHandler('start', self.locationHandler),
                    CommandHandler('option', self.languageHandler)
                ],

                map_to_parent = {
                    ConversationHandler.END:ConversationHandler.END
                }
            )
    #============ Handler, Method ==============#
    '''
    # 일반 함수
    # 챗봇 소개 및 DB 연동
    # 챗봇 명령어 등을 설명하기 위함
    # self.locationHandler에서 호출 됨, callback 함수 이외에 제일 먼저 호출 되는 함수
    '''
    def introduction(self, update:Update):
            update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다. 🙂')

            # DB 연동
            self.user_con = self.user_connection()
            self.message_con = self.message_connection()
            self.create_table(self.user_con)


    '''
    # 일반 함수
    # 챗봇의 사용법을 알려주기 위함
    # self.locationHandler에서 호출 됨
    '''    
    def showHint(self, update:Update):
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

    '''
    # 일반 함수
    # DB에 데이터를 저장하기 위한 함수
    # self.messageHandler에서 호출
    # 반환 값은 사용되지 않음
    '''
    def dbHandler(self, id, language, region):
        # User ID : self.user_id
        # Location : self.location
        # Language : self.language
        user_info = []                  
        user_info.extend([id, language, region])
        self.insert_table(self.user_con, user_info[0], user_info[1], user_info[2])

    '''
    # 일반 함수
    # 버튼 메뉴를 생성하기 위한 함수
    # 복붙 코드라 정확한 기능을 이해하지 못함
    # self.locationHandlerr와 self.languageHandler에서
        InlineKeyboardMarkup 함수의 인자로 사용 됨
    '''
    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    '''
    # 일반 함수
    # 전달된 btnText_list를 이용해 버튼 생성
    '''
    def createButton(self, btnText_list):
        btn_list = []

        for text in btnText_list:
            btn_list.append(InlineKeyboardButton(text, callback_data=text))

        show_markup = InlineKeyboardMarkup(self.build_menu(btn_list, len(btn_list)))
        return show_markup

    '''
    # callback 함수
    # ConversationHandler의 entry_point에 할당 된 Handler에서 호출 됨
    # 즉, 챗봇 시작 시, 가장 먼저 호출 되는 Handler
    # 반환 값을 통해 다음 CallbackQueryHandler를 결정함(ConversationHandler가 자동으로)
    # update.effective_chat.id를 통해 현재 챗봇을 이용 중인 user의 ID를 가져옴
    # show_markup : btn_list를 기반으로 만들어진 버튼 메뉴가 담기는 변수
    '''
    def locationHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id
        self.introduction(update)
        self.showHint(update)
       
        btnText_list = [
            '대전광역시', '충북'
        ]

        context.bot.send_message(
            chat_id=self.user_id, 
            text = '🧭거주하는 지역을 선택해 주세요.', 
            reply_markup = self.createButton(btnText_list)
        )
        return self.LOCATION_BUTTON

    '''
    # callback 함수
    # self.locationHandler 이후 동작(state에서 Return const에 따라 결정 됨) 
    # self.locationHandler을 통해 생성된 버튼(지역)을 누르면 update.callback_query.data에 
        해당 버튼의 callback_data가 저장 됨
    # 반환 값을 통해 다음 CallbackQueryHandler를 결정함(ConversationHandler가 자동으로)
    # show_markup : btn_list를 기반으로 만들어진 버튼 메뉴가 담기는 변수
    '''
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

    '''
    # callback 함수
    # self.languageHandler 이후 동작(state에서 Return const에 따라 결정 됨) 
    # self.locationHandler을 통해 생성된 버튼(지역)을 누르면 update.callback_query.data에 
        해당 버튼의 callback_data가 저장 됨
    # 이 Handler 호출 시점에 self.user_id, self.location, self.language에 값이 들어 가게 됨
    # 따라서, 이 Handler가 호출 되는 시점에, DB에 데이터를 저장하도록 설계함(self.dbControl 함수 호출)
    # message : DB에서 얻어 온 실제 재난 문자가 저장 되는 변수
    '''
    def messageHandler(self, update:Update, context:CallbackContext):
        self.language = update.callback_query.data
        print(self.language)
        # self.dbControl()

        # message = '긴급 재난 문자'

        # # 긴급 재난 문자 전송
        # context.bot.send_message(chat_id=self.user_id,
        #     text=message
        # )
        self.dbHandler(self.user_id, self.language, self.location)
        message = self.search_data(self.message_con, self.language, self.location)

        # 긴급 재난 문자 전송
        for i in range(0, len(message)):
            str_message = str(message[i])
            context.bot.send_message(chat_id=self.user_id,
                text = str_message
            )
    
    '''
    # callback 함수
    # fallback 인자에 들어간 Handler에서 호출하는 callback 함수
    '''
    def fallbackHandler(self, update:Update, context:CallbackContext):
        update.message.reply_text('이용해 주셔서 감사합니다.')

    def user_connection(self):
            try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
                user_con = sqlite3.connect('user_db.db')
                print("[DB] - user db file connect")
                return user_con
            except Error: # 에러 출력
                print(Error)

    def message_connection(self):
            try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
                message_con = sqlite3.connect('message_db.db')
                print("[DB] - message db file connect")
                return message_con
            except Error: # 에러 출력
                print(Error)

    def create_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("CREATE TABLE IF NOT EXISTS user_tb(id INT, language TEXT, region TEXT)")
        con.commit()
        print("[DB] - create")

    def insert_table(self, con, id, language, region):
        cursor_db = con.cursor()
        cursor_db.execute('INSERT INTO user_tb VALUES (?, ?, ?)', (id, language, region,))
        con.commit()
        print("[DB] - insert")

    def clear_table(self, con):
        cursor_db = con.cursor()
        cursor_db.execute("DELETE FROM user_tb")
        con.commit()
        print("[DB] - clear")

    def disconnetion(self, con):
        con.close()
        print("[DB] - disconnet")

    def search_data(self, con, language, region):
        serarch_data = []
        cursor_db = con.cursor()
        print(language, region)
        if region == "대전광역시":
            if language == "영어":
                cursor_db.execute("SELECT *FROM eng_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("Sorry, the latest disaster safety text does not exist.")
            elif language == "일본어":
                cursor_db.execute("SELECT *FROM jp_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
            elif language == "중국어":
                cursor_db.execute("SELECT *FROM ch_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("对不起，最近的灾难安全短信不存在。")

        elif region == "충청북도":
            if language == "영어":
                cursor_db.execute("SELECT *FROM eng_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("Sorry, the latest disaster safety text does not exist.")
            elif language == "일본어":
                cursor_db.execute("SELECT *FROM jp_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
            elif language == "중국어":
                cursor_db.execute("SELECT *FROM ch_tb WHERE region=?", (region,))
                str_data = cursor_db.fetchall()
                for i in range(0, len(str_data)):
                    serarch_data.append(str_data[i][0])
                if len(str_data) == 0:
                    serarch_data.append("对不起，最近的灾难安全短信不存在。")
        else:
            if language == "영어":
                serarch_data.append("Sorry, the latest disaster safety text does not exist.")
            elif language == "일본어":
                serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
            else: # 중국어
                serarch_data.append("对不起，最近的灾难安全短信不存在。")
        print("[DB] - send complete")
        return serarch_data