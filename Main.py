from CornerstoneChatbot import *

bot = CornerstoneChatbot()
bot.updater.dispatcher.add_handler(bot.mainHandler)
bot.updater.start_polling()
# bot.updater.idle()

