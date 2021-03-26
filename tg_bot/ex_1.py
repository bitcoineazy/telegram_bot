import os
from dotenv import load_dotenv
load_dotenv()
from telegram.ext import Updater, Filters, MessageHandler

bot_api_token = os.getenv('bot_api_token')
updater = Updater(token=bot_api_token)

my_id = 534116184

def say_hi(bot, update):
    # В ответ на любое сообщение, переданное в аргумент update,
    # будет отправлено сообщение 'Привет, я бот'
    bot.message.reply_text('Привет, я ботик, у меня баги')

# Регистрируется обработчик MessageHandler;
# из всех полученных сообщений он будет выбирать только текстовые сообщения
# и передавать их в функцию say_hi()
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

# Метод start_polling() запускает процесс polling,
# приложение начнёт отправлять регулярные запросы для получения обновлений.
# updater.start_polling(poll_interval=20.0) - Периодичность опроса
updater.start_polling()