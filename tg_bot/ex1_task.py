import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv
load_dotenv()


bot_api_token = os.getenv('bot_api_token')
TELEGRAM_TOKEN = bot_api_token  # Добавьте токен (не делайте так в реальных проектах!)
CHAT_ID = '534116184'  # Укажите chat_id




bot = telegram.Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=bot_api_token)

def send_message(message):
    text = 'Привет, я ботик, у меня баги'
    bot.send_message(CHAT_ID, text)



# Вызовите функцию здесь
send_message(bot)
#updater.start_polling()