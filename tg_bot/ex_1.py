import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from telegram.ext import Updater, Filters, MessageHandler
load_dotenv()


bot_api_token = os.getenv('bot_api_token')
updater = Updater(token=bot_api_token)

my_id = 534116184


# здесь мы задаем глобальную конфигурацию для всех логеров
logging.basicConfig(
    level=logging.DEBUG,
    filename='logs/bot.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

# а тут настраиваем логгер для текущего файла .py
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)
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