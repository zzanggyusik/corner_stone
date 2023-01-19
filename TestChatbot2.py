from telegram import *
from telegram.ext import *
from ChatbotDB import *
import config

class ChatbotConstants:
    # Conversation State
    REGION_BUTTON = 'Region Button'
    LANGUAGE_BUTTON = 'Language Button'
    END = 'End'

    # Text List Index
    # INTRO = 0
    # SEL_REGION = 1
    # SEL_LANG = 2
    # COMPLETE = 3
    # START = 4
    # SET_INFO = 5
    # HINT = 6
####################################################l
class TestChatbot:
    TOKEN = config.TOKEN
##############################################################
    def __init__(self) -> None:
        self.updater = Updater(TestChatbot.TOKEN)
        self.chatbot_db = ChatbotDB() # connect와 create table 됨

        self.text_list = [
            "Hello, I'm a disaster text translation bot.",
            "Please select the area you live in.",
            "Please select a language to translate.",
            "The setting is complete.",
            "Disaster Text Output",
            "Language and Region Reset",
            "How to use"
        ]

        self.trans_intro = []
        self.trans_region = []
        self.trans_lang = []
        self.trans_complete = []
        self.trans_start = []
        self.trans_info = []
        self.trans_hint = []

        self.mainHandler_conv = ConversationHandler(
            entry_points = [
                CommandHandler('start', self.cb_start),
                CommandHandler('set', self.cb_setRegion)
            ],

            states = {
                ChatbotConstants.REGION_BUTTON : [CallbackQueryHandler(self.cb_setLanguage)],
                ChatbotConstants.LANGUAGE_BUTTON : [
                    CallbackQueryHandler(self.cb_setRegion, pattern = 'back'),
                    CallbackQueryHandler(self.cb_completeSetting)
                ]
            },

            fallbacks = [
                CommandHandler('cancel', self.cb_cancel)
            ],

            map_to_parent = {
                ChatbotConstants.END:ConversationHandler.END
            }
        )
##############################################################
    def sendIntro(self, message: Message) -> None:
        message.reply_text(
            text = self.text_list[ChatbotConstants.INTRO]
        )        

    def createButtons(self, mode) -> InlineKeyboardMarkup:
        buttons = []

        if(mode == ChatbotConstants.REGION_BUTTON):
            buttons = [
                [InlineKeyboardButton("Seoul Metropolitan City", callback_data = '서울특별시')],
                [InlineKeyboardButton("Busan Metropolitan City", callback_data = '부산광역시')],
                [InlineKeyboardButton("Daegu Metropolitan City", callback_data = '대구광역시')],
                [InlineKeyboardButton("Incheon Metropolitan City", callback_data = '인천광역시')],
                [InlineKeyboardButton("Gwangju Metropolitan City", callback_data = '광주광역시')],
                [InlineKeyboardButton("Daejeon Metropolitan City", callback_data = '대전광역시')],
                [InlineKeyboardButton("Ulsan Metropolitan City", callback_data = '울산광역시')],
                [InlineKeyboardButton("Sejong City", callback_data = '세종특별자치시')],
                [InlineKeyboardButton("Gyeonggi Province", callback_data = '경기도')],
                [InlineKeyboardButton("Gangwon-do", callback_data = '강원도')],
                [InlineKeyboardButton("Chungcheongbuk-do", callback_data = '충청북도')],
                [InlineKeyboardButton("Chungcheongnam-do", callback_data = '충청남도')],
                [InlineKeyboardButton("Jeollabuk-do", callback_data = '전라북도')],
                [InlineKeyboardButton("Jeollanam-do", callback_data = '전라남도')],
                [InlineKeyboardButton("Gyeongsangbuk-do Province", callback_data = '경상북도')],
                [InlineKeyboardButton("Gyeongsangnam-do Province", callback_data = '경상남도')],
                [InlineKeyboardButton("Jeju Special Self-Governing Province", callback_data = '제주특별자치도')],
            ]
        elif(mode == ChatbotConstants.LANGUAGE_BUTTON):
            buttons = [
                [
                    InlineKeyboardButton("English", callback_data = 'en'),
                    InlineKeyboardButton("にほんご", callback_data = 'ja')
                ],
                [
                    InlineKeyboardButton("中文", callback_data = 'zh-CN'),
                    InlineKeyboardButton("漢語", callback_data = 'zh-TW')
                ],
                [
                    InlineKeyboardButton("español", callback_data = 'es'),
                    InlineKeyboardButton("français", callback_data = 'fr')
                ],
                [
                    InlineKeyboardButton("das Deutsche", callback_data = 'de'),
                    InlineKeyboardButton("Русский", callback_data = 'ru')
                ],
                [
                    InlineKeyboardButton("Português", callback_data = 'pt'),
                    InlineKeyboardButton("italiàno", callback_data = 'it')
                ],
                [
                    InlineKeyboardButton("Tiếng Việt", callback_data = 'vi'),
                    InlineKeyboardButton("ภาษาไทย", callback_data = 'th')
                ],
                [
                    InlineKeyboardButton("Bahasa Indonesia", callback_data = 'id'),
                    InlineKeyboardButton("बहसा इंडोनेशिया", callback_data = 'hi')
                ],
            ]
        else:
            pass

        return InlineKeyboardMarkup(buttons)

    def sendMessageFromSim(self):
        if self.chatbot_db.visited_user():
            messages = self.chatbot_db.search_data(1)
            for m in messages:
                self.updater.bot.send_message(
                    chat_id = self.chatbot_db.user_id,
                    text = m
                )

##############################################################
    def cb_start(self, update: Update, context: CallbackContext):
        self.chatbot_db.user_id = update.effective_user.id
        user_default_lang = update.effective_user.language_code

        # TODO : PEx.TransMessage(messageList, en, user_default_lang)를 통해 
        #        번역된 메뉴 메시지들을 출력

        self.trans_intro = PEx.TransMessage(self.text_list[0], 'en', user_default_lang)
        self.trans_region = PEx.TransMessage(self.text_list[1], 'en', user_default_lang)
        self.trans_lang = PEx.TransMessage(self.text_list[2], 'en', user_default_lang)
        self.trans_complete = PEx.TransMessage(self.text_list[3], 'en', user_default_lang)
        self.trans_start = PEx.TransMessage(self.text_list[4], 'en', user_default_lang)
        self.trans_info = PEx.TransMessage(self.text_list[5], 'en', user_default_lang)
        self.trans_hint = PEx.TransMessage(self.text_list[6], 'en', user_default_lang)

        self.sendIntro(message = update.message)
        self.cb_sendHint(update, context)

        return ChatbotConstants.END

    # 1. DB와 연결된 상태에서, 정보가 있다면, 재설정 하겠냐고 물어보기
    # 2. DB에 정보가 없다면 정보 입력 
    def cb_setRegion(self, update: Update, context: CallbackContext):
        self.chatbot_db.user_id = update.effective_user.id
        print(self.chatbot_db.user_id)

        text = self.trans_intro
        reply_markup = self.createButtons(ChatbotConstants.REGION_BUTTON)

        # 없을 경우 메뉴 출력
        if update.callback_query == None:  
            update.message.reply_text(
                text = text,
                reply_markup = reply_markup
            )
        else:
            update.callback_query.edit_message_text(
                text = text,
                reply_markup = reply_markup
            )

        return ChatbotConstants.REGION_BUTTON

    def cb_setLanguage(self, update: Update, context: CallbackContext):
        self.chatbot_db.user_id = update.effective_user.id

        update.callback_query.answer()
        self.chatbot_db.user_region = update.callback_query.data
        print('[Bot] : save user region data')

        update.callback_query.edit_message_text(
            text = self.trans_lang,
            reply_markup = self.createButtons(ChatbotConstants.LANGUAGE_BUTTON)
        )

        return ChatbotConstants.LANGUAGE_BUTTON

    def cb_completeSetting(self, update: Update, context: CallbackContext):
        self.chatbot_db.user_id = update.effective_user.id

        update.callback_query.answer()
        self.chatbot_db.user_language_code = update.callback_query.data
        print('[Bot] : save user language code data')

        self.chatbot_db.insert_table()
        
        update.callback_query.edit_message_text(
            text = self.trans_complete
        )

        return ChatbotConstants.END

    def cb_cancel(self, update: Update, context: CallbackContext):
        return ChatbotConstants.END
##############################################################
    def cb_sendHint(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            text = self.hint
        )
        update.message.reply_text('< Menu >\n'+"'/start' | "+self.trans_start+"\n '/set'  | "+self.trans_info+"\n'/help' | "+self.trans_hint+"\n")

##############################################################
def main() -> None:
    bot = TestChatbot()
    bot.updater.dispatcher.add_handler(bot.mainHandler_conv)
    bot.updater.dispatcher.add_handler(CommandHandler('help', bot.cb_sendHint))
    bot.updater.start_polling()
    bot.updater.idle()

if __name__ == '__main__':
    main()