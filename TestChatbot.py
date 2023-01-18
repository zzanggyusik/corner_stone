import telegram
from telegram import *
from telegram.ext import *
from ChatbotDB import *

class ChatbotConstants:
    REGION_BUTTON = 'Region Button'
    LANGUAGE_BUTTON = 'Language Button'
    YES_NO_BUTTON = 'Yes or No'
    END = 'End'

class TestChatbot:
    TOKEN = '5816928241:AAEOJisRYhwP64tckKU7J5BLc7QXwKLi_to'
##############################################################
    def __init__(self) -> None:
        self.updater = Updater(TestChatbot.TOKEN)
        self.chatbot_db = ChatbotDB()

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
            text = '안녕하세요. 긴급 재난 문자 번역 봇입니다.'
        )

    def createButtons(self, mode) -> InlineKeyboardMarkup:
        buttons = []

        if(mode == ChatbotConstants.REGION_BUTTON):
            buttons = [
                [
                    InlineKeyboardButton('대전광역시', callback_data = 'DJ'),
                    InlineKeyboardButton('충청북도', callback_data = 'CB'),
                ]
            ]
        elif(mode == ChatbotConstants.LANGUAGE_BUTTON):
            buttons = [
                [InlineKeyboardButton('english', callback_data = 'en')],
                [InlineKeyboardButton('日本語', callback_data = 'ja')],
                [InlineKeyboardButton('中文 (简体)', callback_data = 'zh-CN')],
                [InlineKeyboardButton('中文 (繁體)', callback_data = 'zh-TW')],
                [InlineKeyboardButton('back', callback_data = 'back')]
            ]
        elif(mode == ChatbotConstants.YES_NO_BUTTON):
            buttons = [
                [
                    InlineKeyboardButton('예', callback_data = 'yes'),
                    InlineKeyboardButton('아니요', callback_data = 'no')
                ]
            ]
        else:
            pass

        return InlineKeyboardMarkup(buttons)

    def sendMessageFromSim(self):
        # DB에서 재난 문자 긁어 오기 DB쪽 함수 호출 해야함
        # text: list = PEx.transMessage(DB에서 긁어온 메시지 리스트 형태)
        # upda
        # for t in text:
        #     self.updater.bot.send_message(
        #         #chat_id = DB.user_id,
        #         #text = t
        #     )
        pass

##############################################################
    def cb_start(self, update: Update, context: CallbackContext):
        self.chatbot_db.user_id = update.effective_user.id


        # 아래 두 함수는 정보가 있든 없든 출력
        self.sendIntro(message = update.message)
        self.cb_sendHint(update, context)

        return ChatbotConstants.END

    # 1. DB와 연결된 상태에서, 정보가 있다면, 재설정 하겠냐고 물어보기
    # 2. DB에 정보가 없다면 정보 입력 
    def cb_setRegion(self, update: Update, context: CallbackContext):
        self.chatbot_db.user_id = update.effective_user.id
        print(self.chatbot_db.user_id)

        if self.chatbot_db.visited_user():
            update.message.reply_text(
                text = '번역 받으실 언어를 변경하시겠습니까?',
                reply_markup = self.createButtons(ChatbotConstants.YES_NO_BUTTON)
            )
            return ChatbotConstants.END

        text = '거주하시는 지역을 선택하세요.'
        reply_markup = self.createButtons(ChatbotConstants.REGION_BUTTON)
        # DB에 정보가 있는지 확인

        # 있을 경우 return IS_INFO를 반환하여 Conversation Handler에서 다른 callback 호출

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
        # DB에 Region 값 저장(갱신) "update.callback_query.data"
        update.callback_query.edit_message_text(
            text = '번역 받으실 언어를 선택해 주세요.',
            reply_markup = self.createButtons(ChatbotConstants.LANGUAGE_BUTTON)
        )

        return ChatbotConstants.LANGUAGE_BUTTON

    def cb_completeSetting(self, update: Update, context: CallbackContext):
        # DB에 Language 값 저장(갱신) "update.callback_query.data"
        print(update.callback_query.data)
        
        update.callback_query.edit_message_text(
            text = '세팅이 완료됐습니다.'
        )

        update.callback_query.message.reply_text(
            text = '메시지 보내는 중...'
        )

        update.callback_query.message.reply_text(
            text = '긴급 재난 문자입니다.'
        )
        return ChatbotConstants.END

    def cb_cancel(self, update: Update, context: CallbackContext):
        pass
    
##############################################################
    def cb_sendHint(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            text = '/start - 챗봇 시작(메시지 전송)\n' 
                + '/help - 사용법 설명\n'
                + '/set - 지역, 언어 설정'
        )
##############################################################
def main() -> None:
    bot = TestChatbot()
    bot.updater.dispatcher.add_handler(bot.mainHandler_conv)
    bot.updater.dispatcher.add_handler(CommandHandler('help', bot.cb_sendHint))
    bot.updater.start_polling()
    bot.updater.idle()

if __name__ == '__main__':
    main()