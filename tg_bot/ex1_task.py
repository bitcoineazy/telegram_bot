import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv
load_dotenv()


TELEGRAM_TOKEN = os.getenv('bot_api_token')
CHAT_ID = '534116184'




bot = telegram.Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN)

def send_message(message):
    text = 'Привет, я ботик, у меня баги'
    bot.send_message(CHAT_ID, text)



# Вызовите функцию здесь
send_message(bot)
#updater.start_polling()