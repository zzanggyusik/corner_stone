#수정#fail
from telegram import *
from telegram.ext import CommandHandler
from telegram.ext import *
import prettytable as pt
from sqlite3 import Error
import sqlite3

TOKEN = "5620332585:AAE6riueZPkYVu3y_v3z5rg3ozaK68ys-Ho"

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
        self.mainHandler = ConversationHandler(
                entry_points = [
                    CommandHandler('start', self.locationButtonHandler)
                ],

                states = {
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageHandler)],
                    self.LANGUAGE_BUTTON : [CallbackQueryHandler(self.messageHandler)]
                },

                fallbacks = [
                    CommandHandler('cancel',self.fallbackHandler),
                    CommandHandler('start', self.locationButtonHandler),
                    CommandHandler('option', self.languageHandler),
                    CommandHandler('message', self.messageHandler2)
                ],

                map_to_parent = {
                    ConversationHandler.END:ConversationHandler.END
                }
            )
    #============ Handler, Method ==============#

    def introduction(self, update:Update):
            update.message.reply_text('안녕하세요, 코너스톤 챗봇입니다 🙂')

            #table을 통한 출력
            table = pt.PrettyTable(['function', 'input'])
            table.align['function'] = 'm'
            table.align['input'] = 'm'

            data = [
                ('start','/start '),
                ('option','/option'),
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

    def build_menu(self, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

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
        self.dbHandler(self.user_id, self.language, self.location)
        
        update.message.reply_text('"/message"를 입력해주세요.')


    def messageHandler2(self, update:Update, context:CallbackContext):
    
        message = self.search_data(self.message_con, self.language, self.location)
        # 긴급 재난 문자 전송

        message = '긴급 재난 문자'

        # 긴급 재난 문자 전송
        context.bot.send_message(chat_id=self.user_id,
            text=message
        )
        # for i in range(0, len(message)):
        #     str_message = str(message[i])
        #     context.bot.send_message(chat_id=self.user_id,
        #         text = str_message
        #     )

    def fallbackHandler(self, update:Update, context:CallbackContext):
        update.message.reply_text('이용해 주셔서 감사합니다.')

    # def user_connection(self):
    #         try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
    #             user_con = sqlite3.connect('user_db.db')
    #             print("[DB] - user db file connect")
    #             return user_con
    #         except Error: # 에러 출력
    #             print(Error)

    # def message_connection(self):
    #         try: # 데이터베이스 연결 (파일이 없으면 만들고 있으면 연결)
    #             message_con = sqlite3.connect('message_db.db')
    #             print("[DB] - message db file connect")
    #             return message_con
    #         except Error: # 에러 출력
    #             print(Error)

    # def create_table(self, con):
    #     cursor_db = con.cursor()
    #     cursor_db.execute("CREATE TABLE IF NOT EXISTS user_tb(id INT, language TEXT, region TEXT)")
    #     con.commit()
    #     print("[DB] - create")

    # def insert_table(self, con, id, language, region):
    #     cursor_db = con.cursor()
    #     cursor_db.execute('INSERT INTO user_tb VALUES (?, ?, ?)', (id, language, region,))
    #     con.commit()
    #     print("[DB] - insert")

    # def clear_table(self, con):
    #     cursor_db = con.cursor()
    #     cursor_db.execute("DELETE FROM user_tb")
    #     con.commit()
    #     print("[DB] - clear")

    # def disconnetion(self, con):
    #     con.close()
    #     print("[DB] - disconnet")

    # def search_data(self, con, language, region):
    #     serarch_data = []
    #     cursor_db = con.cursor()
    #     print(language, region)
    #     if region == "대전광역시":
    #         if language == "영어":
    #             cursor_db.execute("SELECT *FROM eng_tb WHERE region=?", (region,))
    #             str_data = cursor_db.fetchall()
    #             for i in range(0, len(str_data)):
    #                 serarch_data.append(str_data[i][0])
    #             if len(str_data) == 0:
    #                 serarch_data.append("Sorry, the latest disaster safety text does not exist.")
    #         elif language == "일본어":
    #             cursor_db.execute("SELECT *FROM jp_tb WHERE region=?", (region,))
    #             str_data = cursor_db.fetchall()
    #             for i in range(0, len(str_data)):
    #                 serarch_data.append(str_data[i][0])
    #             if len(str_data) == 0:
    #                 serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
    #         elif language == "중국어":
    #             cursor_db.execute("SELECT *FROM ch_tb WHERE region=?", (region,))
    #             str_data = cursor_db.fetchall()
    #             for i in range(0, len(str_data)):
    #                 serarch_data.append(str_data[i][0])
    #             if len(str_data) == 0:
    #                 serarch_data.append("对不起，最近的灾难安全短信不存在。")

    #     elif region == "충청북도":
    #         if language == "영어":
    #             cursor_db.execute("SELECT *FROM eng_tb WHERE region=?", (region,))
    #             str_data = cursor_db.fetchall()
    #             for i in range(0, len(str_data)):
    #                 serarch_data.append(str_data[i][0])
    #             if len(str_data) == 0:
    #                 serarch_data.append("Sorry, the latest disaster safety text does not exist.")
    #         elif language == "일본어":
    #             cursor_db.execute("SELECT *FROM jp_tb WHERE region=?", (region,))
    #             str_data = cursor_db.fetchall()
    #             for i in range(0, len(str_data)):
    #                 serarch_data.append(str_data[i][0])
    #             if len(str_data) == 0:
    #                 serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
    #         elif language == "중국어":
    #             cursor_db.execute("SELECT *FROM ch_tb WHERE region=?", (region,))
    #             str_data = cursor_db.fetchall()
    #             for i in range(0, len(str_data)):
    #                 serarch_data.append(str_data[i][0])
    #             if len(str_data) == 0:
    #                 serarch_data.append("对不起，最近的灾难安全短信不存在。")
    #     else:
    #         if language == "영어":
    #             serarch_data.append("Sorry, the latest disaster safety text does not exist.")
    #         elif language == "일본어":
    #             serarch_data.append("申し訳ありませんが、最近災害安全メールが存在しません。")
    #         else: # 중국어
    #             serarch_data.append("对不起，最近的灾难安全短信不存在。")
    #     print("[DB] - send complete")
    #     return serarch_data

bot = CornerstoneChatbot()
updater = Updater(TOKEN)
updater.dispatcher.add_handler(bot.mainHandler)
updater.start_polling()
updater.idle()