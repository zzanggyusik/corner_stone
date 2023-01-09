from TelegramChatbot9 import *

bot = CornerstoneChatbot()
bot.updater.dispatcher.add_handler(bot.mainHandler)
bot.updater.start_polling()