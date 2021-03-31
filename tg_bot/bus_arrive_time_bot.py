# Will add user interface to add their own routes later
import os
import time

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from dotenv import load_dotenv

load_dotenv()

YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_BUS')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://api.rasp.yandex.net/v3.0/search/'
HEADERS = {'Authorization': f'OAuth {YANDEX_TOKEN}'}
STATIONS = [os.getenv('HOME_STATION'), os.getenv('SUB_STATION')]
FIRST_STATE, SECOND_STATE = range(2)  # Этапы разговора
POIM_TUSH = 0


def parse_all_routes_list(all_routes):
    parsed_routes = []
    time_get = time.time()
    time_iso8601 = time.localtime(time_get)
    hour = int(time.strftime('%H', time_iso8601))
    needed_idx = [i for i, word in enumerate(all_routes.keys())
                  if word.startswith(f'{hour if hour > 10 else f"0{hour}"}')
                  or word.startswith(f'{(hour + 1) if (hour + 1) > 10 else f"0{hour + 1}"}')]
    list_all_routes = list(all_routes.keys())
    for each_index in needed_idx:
        parsed_routes.append(list_all_routes[each_index])
    return parsed_routes[:20]


def poyma_tushin(update, context):
    print('poyma-tushin')
    route = f'{update.callback_query.message.reply_markup}'
    all_routes = {}  # Все маршруты в нотации время отправления : номер маршрута
    try:
        if 'Пойма - Тушинская' in route:
            arrive_list = requests.get(URL, params={
                'apikey': YANDEX_TOKEN,
                'from': STATIONS[0],
                'to': STATIONS[1],
                'transport_types': 'bus',
                'limit': 400,
            })
            arrive_list_json = arrive_list.json()
            for i in range(len(arrive_list_json.get('segments'))):
                all_routes.update(
                    {arrive_list_json.get('segments')[i].get('departure'):
                         arrive_list_json.get('segments')[i].get('thread').get('number')})
            parsed_routes = parse_all_routes_list(all_routes)
            context.bot.send_message(CHAT_ID, '\n'.join(parsed_routes))
            # update.message.reply_text(text='\n'.join(parsed_routes))
        if 'Тушинская - Пойма' in route:
            arrive_list = requests.get(URL, params={
                'apikey': YANDEX_TOKEN,
                'from': STATIONS[1],
                'to': STATIONS[0],
                'transport_types': 'bus',
                'limit': 400,
            })
            arrive_list_json = arrive_list.json()
            for i in range(len(arrive_list_json.get('segments'))):
                all_routes.update(
                    {arrive_list_json.get('segments')[i].get('departure'):
                         arrive_list_json.get('segments')[i].get('thread').get('number')})
            parsed_routes = parse_all_routes_list(all_routes)
            context.bot.send_message(CHAT_ID, '\n'.join(parsed_routes))
    except Exception as e:
        error_message = f'Бот столкнулся с ошибкой: {e}'
        time.sleep(5)


def tushin_poyma(update, context):
    pass

def start(update, context):
    user = update.message.from_user
    print(f'Пользователь {user.first_name} начал разговор')
    keyboard = [
        [
            InlineKeyboardButton('Пойма - Тушинская', callback_data=str(POIM_TUSH))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text='Добро пожаловать в моего бота! Выберите маршрут', reply_markup=reply_markup
    )
    # Сообщаем ConversationHandler, что сейчас состояние FIRST_STATE
    return FIRST_STATE


def re_start(update, context):
    # Получаем `CallbackQuery` из обновления `update`
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Пойма - Тушинская', callback_data=str(POIM_TUSH))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отредактируем сообщение, вызвавшее обратный вызов.
    # Это создает ощущение интерактивного меню.
    query.edit_message_text(
        text='Выберите маршрут', reply_markup=reply_markup
    )
    return FIRST_STATE


def end(update, _):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main():
    bot_client = Updater(token=f'{TELEGRAM_TOKEN}')
    while True:
        try:
            conv_handler = ConversationHandler(
                entry_points=[CommandHandler('start', start)],
                states={
                    FIRST_STATE: [
                        CallbackQueryHandler(poyma_tushin, pattern='^' + str(POIM_TUSH) + '$'),
                    ],
                    SECOND_STATE: [
                        CallbackQueryHandler(re_start, pattern='^' + str(POIM_TUSH) + '$'),
                    ],
                },
                fallbacks=[CommandHandler('start', start)],
            )

            bot_client.dispatcher.add_handler(conv_handler)
            # tushka_handler = CommandHandler('tushka', get_arrive_list_poyma_tushin)
            # bot_client.dispatcher.add_handler(tushka_handler)
            bot_client.start_polling()
            bot_client.idle()
        except Exception as e:
            error_message = f'Бот столкнулся с ошибкой: {e},'
            time.sleep(5)


if __name__ == '__main__':
    main()
