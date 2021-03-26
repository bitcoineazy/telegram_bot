import os
import telebot
from telegram import Bot
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv
import logging

load_dotenv()
import time

bot_api_token = os.getenv('bot_api_token')
my_id = 534116184

# bot = Bot(token=bot_api_token)
# Отправка сообщения
chat_id = 534116184
oleg = 195995110

updater = Updater(token=f'{bot_api_token}')


def ghoul(update, context):
    context.bot.send_message(oleg, 'Ты раб!')
    time.sleep(3)
    x = 1000
    while x >= 7:
        time.sleep(1)
        text = f'{x} - 7'
        context.bot.send_message(oleg, text)
        x -= 7
    else:
        context.bot.send_message(oleg, 'Туцтуцтуц')

start_handler = CommandHandler('start', ghoul)
dispatcher = updater.dispatcher
updater.dispatcher.add_handler(start_handler)
updater.start_polling()
