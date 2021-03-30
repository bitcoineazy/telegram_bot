# Will add some cool bus arriving time bot for my route
# Will do some Starline API for TAXI here
import os
import time

import requests
import telegram
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

load_dotenv()

YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_BUS')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://api.rasp.yandex.net/v3.0/search/'
HEADERS = {'Authorization': f'OAuth {YANDEX_TOKEN}'}
STATIONS = [os.getenv('HOME_STATION'), os.getenv('SUB_STATION')]


def parse_all_routes_list(all_routes):

    parsed_routes = all_routes


def get_arrive_list():
    all_routes = {}  # Все маршруты в нотации время отправления : номер маршрута
    time_get = time.time()
    time_iso8601 = time.ctime(time_get)
    print(time_iso8601)
    try:
        print()
        arrive_list = requests.get(URL, params={
            'apikey': YANDEX_TOKEN,
            'from': STATIONS[0],
            'to': STATIONS[1],
            'transport_types': 'bus',
            'limit': 500,
        })
        arrive_list_json = arrive_list.json()
        for i in range(len(arrive_list_json.get('segments'))):
            all_routes.update(
                {arrive_list_json.get('segments')[i].get('departure'):
                 arrive_list_json.get('segments')[i].get('thread').get('number')})
        return all_routes
    except Exception as e:
        error_message = f'Бот столкнулся с ошибкой: {e}'
        time.sleep(5)


def send_message(message, bot_client):
    # logging.info(f'Sent message: {message}, to user: {CHAT_ID}')
    # return bot_client.send_message(CHAT_ID, message)
    pass


def main():

    bot_client = Updater(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            all_routes = get_arrive_list()
            print(all_routes)

            '''if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(
                        new_homework.get('homeworks')[0]),
                    bot_client)
            current_timestamp = new_homework.get(
                'current_date', current_timestamp)  # обновить timestamp
            time.sleep(300)  # опрашивать раз в 5 минут'''
            time.sleep(300)
        except Exception as e:
            error_message = f'Бот столкнулся с ошибкой: {e},'
            # send_message(error_message, bot_client)
            time.sleep(5)


if __name__ == '__main__':
    main()
