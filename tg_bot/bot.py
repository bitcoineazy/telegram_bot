import os
from telegram import Bot
from dotenv import load_dotenv
load_dotenv()


bot_api_token = os.getenv('bot_api_token')
my_id = 534116184

bot = Bot(token=bot_api_token)
# Отправка сообщения
chat_id = 534116184
text = 'Вам телеграмма!'
bot.send_message(chat_id, text)