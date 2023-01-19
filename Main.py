from CornerstoneChatbot import *

bot = CornerstoneChatbot()
updater = Updater('5936320630:AAGPcpJQfVwN6V5aYMstT1jBkvwn2hhsubI')
updater.dispatcher.add_handler(bot.mainHandler)

updater.start_polling()
updater.idle()
