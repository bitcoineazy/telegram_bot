# Will do some Starline API for TAXI here
import os
import time

import logging
import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}

logging.basicConfig(
    level=logging.DEBUG,
    filename='logs/bot.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework_name is None:
        return 'Пришли пустые данные homework_name'
    homework_status = homework.get('status')
    if homework_status is None:
        return 'Пришли пустые данные homework_status'
    if homework_status != 'approved':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = ('Ревьюеру всё понравилось,'
                   ' можно приступать к следующему уроку.')
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    try:
        homework_statuses = requests.get(
            URL, headers=HEADERS, params={
                'from_date': current_timestamp
                if current_timestamp is not None
                else int(time.time())})
        return homework_statuses.json()
    except Exception as e:
        error_message = f'Бот столкнулся с ошибкой: {e}, Лог: {logging.ERROR}'
        logging.error(error_message)
        time.sleep(5)


def send_message(message, bot_client):
    logging.info(f'Sent message: {message}, to user: {CHAT_ID}')
    return bot_client.send_message(CHAT_ID, message)


def main():
    bot_start_debug_log = logging.getLogger('BotStart')
    bot_start_debug_log.setLevel(logging.DEBUG)
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(
                        new_homework.get('homeworks')[0]),
                    bot_client)
            current_timestamp = new_homework.get(
                'current_date', current_timestamp)  # обновить timestamp
            time.sleep(300)  # опрашивать раз в 5 минут

        except Exception as e:
            error_message = (f'Бот столкнулся с ошибкой: {e},'
                             f' Лог: {logging.ERROR}')
            send_message(error_message, bot_client)
            time.sleep(5)


if __name__ == '__main__':
    main()
