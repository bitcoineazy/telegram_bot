# Will add some cool bus arriving time bot for my route
# Will do some Starline API for TAXI here
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://api.rasp.yandex.net/v3.0/search/'
HEADERS = {'Authorization': f'OAuth {YANDEX_TOKEN}'}
STATIONS = [os.getenv('HOME_STATION'), os.getenv('SUB_STATION')]


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')



def get_arrive_list():
    try:
        arrive_list = requests.get(URL, params={
            'apikey': YANDEX_TOKEN,
            'from': STATIONS[0],
            'to': STATIONS[1],
            'transport_types': 'bus',
            'limit': 10,
        })
        return arrive_list.json()
    except Exception as e:
        error_message = f'Бот столкнулся с ошибкой: {e}'
        time.sleep(5)


def send_message(message, bot_client):
    #logging.info(f'Sent message: {message}, to user: {CHAT_ID}')
    #return bot_client.send_message(CHAT_ID, message)
    pass

def main():
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            all_schedule = get_arrive_list()
            for i in range(5):
                print(all_schedule['segments'][i].get('arrival'), f'arrival {i}')
                print(all_schedule['segments'][i].get('departure'), f'departure {i}')
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
            #send_message(error_message, bot_client)
            time.sleep(5)


if __name__ == '__main__':
    main()
