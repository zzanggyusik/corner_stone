from CornerstoneChatbot import *

bot = CornerstoneChatbot()
# updater = Updater('5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI')
# updater.dispatcher.add_handler(bot.mainHandler)
bot.updater.dispatcher.add_handler(bot.mainHandler)

bot.updater.start_polling()
# bot.updater.idle()


print('is Stop')
# b = telegram.Bot('5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI')
# b.send_message(chat_id=bot.user_id, text='send')
