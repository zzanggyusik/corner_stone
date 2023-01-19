import telegram
from telegram import *
from telegram.ext import CommandHandler
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
        self.user_id = ''           #사용자의 ID, self.locationHandler에서 값이 저장 됨
        self.location = ''          #선택한 지역, self.languageHandler에서 값이 저장 됨
        self.language = ''          #선택한 언어, self.messageHandler에서 값이 저장 됨
        #=========== Simulation Data ===========#
        self.post_num = ''          #시뮬레이션 정보
        #============ Return const =============#
        self.LOCATION_BUTTON = 1    #지역 선택 함수(locationHandler) 리턴값
        self.LANGUAGE_BUTTON = 2    #언어 선택 함수(languageHandler) 리턴값
        #=============== Contant ===============#
        self.isAlready = False      #사용자 아이디 정보, 처음 False로 설정
        #================ Main =================#
        #ConversationHandler를 통한 Handler흐름 제어
        self.mainHandler = ConversationHandler(
                #각 이벤트에 대한 CommandHandler생성(command[명령어], callback[응답])
                #entry_point : 챗봇 시작, 가장 먼저 실행되는 Handler // 처음 시작
                entry_points = [
                    CommandHandler('start', self.locationHandler),
                ],

                #states : return const에 따라 호출되는 Handler
                states = {
                    #지역 버튼 선택 시 언어 버튼 응답
                    self.LOCATION_BUTTON : [CallbackQueryHandler(self.languageHandler)],
                    #언어 버튼 선택 시 메시지 응답
                    self.LANGUAGE_BUTTON : [CallbackQueryHandler(self.messageHandler)],
                },

                #falbacks : 순서 무관하여 조건 만족시 Handler // 입력 시 나오게 하는 값
                fallbacks = [
                    #입력: start -> 지역 선택(처음만)
                    CommandHandler('start', self.locationHandler),  # start
                    CommandHandler('reset',self.resetHandler),
                    #CommandHandler('change', self.languageHandler),  # mode 변경 필요
                ],

                map_to_parent = {
                    ConversationHandler.END:ConversationHandler.END
                }
            )
    #=============== Method ==================#
    #시작, 메시지 출력
    def introduction(self, update:Update):
        update.message.reply_text('안녕하세요, 긴급 재난 문자 번역을 수행하는 코너스톤 챗봇입니다.🙂')
        update.message.reply_text("'/start' : start\n'/set' : reset\n'/help' : menu")

    #메시지 보내기(시뮬, db연동)
    def sendMessageWithSim(self):
        #존재하지 않는 아이디인 경우 db값에 저장 후 True로 바꿈
        if(self.isAlready == False):
            if(self.chatbot_db.visited_user(self.chatbot_db.con, self.user_id)):
                self.isAlready = True

        #이미 존재하는 아이디인 경우 알맞은 db에서 알맞은 정보 찾아 메시지 발송
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

    #메시지 보내기
    #db내용 저장 // 메시지 보내기 (기본)
    def mySendMessage(self, update:Update, context:CallbackContext):
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
    
    #지역 설정 버튼
    def locationHandler(self, update:Update, context:CallbackContext):
        
        #chat_id 가져옴
        self.user_id = update.effective_chat.id
        #db랑 연동
        self.chatbot_db.con = self.chatbot_db.connection()
        self.language = self.chatbot_db.user_language(self.chatbot_db.con, self.user_id)
        self.location = self.chatbot_db.user_location(self.chatbot_db.con, self.user_id)
        
        #사용자 ID가 존재하는 경우, LANGAUGE_BUTTON리턴 --> 메시지 출력
        if  self.chatbot_db.visited_user(
            self.chatbot_db.con,
            self.user_id
        ) == True:
            self.mySendMessage(update=update, context=context)
            return self.LANGUAGE_BUTTON

        #존재하지 않는 경우 기본 버튼 선택 출력하도록 함
        #instruction함수 호출
        self.introduction(update)
        
        #버튼 메뉴
        btnText_list = [
            [InlineKeyboardButton("Seoul Metropolitan City", callback_data = 'seo')],
            [InlineKeyboardButton("Busan Metropolitan City", callback_data = 'bu')],
            [InlineKeyboardButton("Daegu Metropolitan City", callback_data = 'da')],
            [InlineKeyboardButton("Incheon Metropolitan City", callback_data = 'in')],
            [InlineKeyboardButton("Gwangju Metropolitan City", callback_data = 'gw')],
            [InlineKeyboardButton("Daejeon Metropolitan City", callback_data = 'de')],
            [InlineKeyboardButton("Ulsan Metropolitan City", callback_data = 'ul')],
            [InlineKeyboardButton("Sejong City", callback_data = 'se')],
            [InlineKeyboardButton("Gyeonggi Province", callback_data = 'gu')],
            [InlineKeyboardButton("Gangwon-do", callback_data = 'ga')],
            [InlineKeyboardButton("Chungcheongbuk-do", callback_data = 'cb')],
            [InlineKeyboardButton("Chungcheongnam-do", callback_data = 'cn')],
            [InlineKeyboardButton("Jeollabuk-do", callback_data = 'jb')],
            [InlineKeyboardButton("Jeollanam-do", callback_data = 'jn')],
            [InlineKeyboardButton("Gyeongsangbuk-do Province", callback_data = 'gb')],
            [InlineKeyboardButton("Gyeongsangnam-do Province", callback_data = 'gn')],
            [InlineKeyboardButton("Jeju Special Self-Governing Province", callback_data = 'je')],

        ]
        reply_markup = InlineKeyboardMarkup(btnText_list)
        update.message.reply_text('🧭거주 지역 선택',reply_markup = reply_markup)

        print(self.location)

        return self.LOCATION_BUTTON
    
    #언어 설정 버튼
     # show_markup : btn_list를 기반으로 만들어진 버튼 메뉴가 담기는 변수
    def languageHandler(self, update:Update, context:CallbackContext):
        query = update.callback_query
        print('지역',self.location)
        print(update.callback_query.data)
        #chat_id불러옴
        self.user_id = update.effective_chat.id
        #callback_query: 응답 // 응답 없을때, 지속적으로 저장하게 함(전데이터)
        if update.callback_query != None:
            print('init self.location!')
            self.location = update.callback_query.data
            print('w', self.location)

        #버튼 생성
        btnText_list = [
            [InlineKeyboardButton("English", callback_data = 'en'),
            InlineKeyboardButton("にほんご", callback_data = 'ja')],
            [InlineKeyboardButton("中文", callback_data = 'zh-chs'),
            InlineKeyboardButton("漢語", callback_data = 'zh-cht')],
            [InlineKeyboardButton("español", callback_data = 'es'),
            InlineKeyboardButton("français", callback_data = 'fr')],
            [InlineKeyboardButton("das Deutsche", callback_data = 'de'),
            InlineKeyboardButton("Русский", callback_data = 'ru')],
            [InlineKeyboardButton("Português", callback_data = 'pt'),
            InlineKeyboardButton("italiàno", callback_data = 'it')],
            [InlineKeyboardButton("Tiếng Việt", callback_data = 'vi'),
            InlineKeyboardButton("ภาษาไทย", callback_data = 'th')],
            [InlineKeyboardButton("Bahasa Indonesia", callback_data = 'id'),
            InlineKeyboardButton("बहसा इंडोनेशिया", callback_data = 'hi')],
        ]
        reply_markup = InlineKeyboardMarkup(btnText_list)
        update.callback_query.message.reply_text('🧭사용 언어 선택', reply_markup = reply_markup)

        print(self.language)

        return self.LANGUAGE_BUTTON

    #메시지 출력
    # message : DB에서 얻어 온 실제 재난 문자가 저장 되는 변수
    def messageHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id
        if update.callback_query != None:
            print('init self.language')
            self.language = update.callback_query.data

        print(self.language)
        #db연동
        self.chatbot_db.dbHandler(
            self.user_id, 
            self.language, 
            self.location
        )   

        self.mySendMessage(update=update, context=context)
        self.isAlready = True
        
    #db에 저장된 내용 초기화
    def resetHandler(self, update:Update, context:CallbackContext):
        self.user_id = update.effective_chat.id

        self.chatbot_db.remove_id(
            self.chatbot_db.con,
            self.user_id
        )

        context.bot.send_message(
                chat_id=self.user_id,
                text = "초기화 되었습니다.\n재설정은 '/start' 를 입력해주세요."
        )

## db연동시 인자 값 전달 받을때 어려움
## 값 저장에서 비어있는 경우에 불러오는 것, None설정
