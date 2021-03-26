import os
from pyrogram import Client
from dotenv import load_dotenv
load_dotenv()

api_id = os.getenv('client_api_id')
api_hash = os.getenv('client_api_hash')

with Client('my_account', api_id, api_hash) as app:
    # Первый параметр метода send_message — id (int) или имя (str) того пользователя,
    # которому будет отправлено сообщение.
    # Зарезервированное слово "me" означает ваш собственный аккаунт.
    app.send_message('me', 'Привет себе будущему!')

