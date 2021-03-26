import os
import requests
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

bot_api_token = os.getenv('bot_api_token')
my_id = 534116184
#print(bot_api_token)

bot_api = requests.get(f'https://api.telegram.org/bot{bot_api_token}/sendMessage?chat_id={my_id}&text=привет')  # отправка сообщения
#bot_api_1 = requests.get(f'https://api.telegram.org/bot{bot_api_token}/getMe')
bot_getupdates = requests.get(f'https://api.telegram.org/bot{bot_api_token}/getUpdates')  # обновления
pprint(bot_getupdates.text)