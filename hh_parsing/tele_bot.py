import telebot
import pandas as pd
from datetime import date
from telebot import types
import json


# take telegram token
with open("data/telegram_token.txt", "r") as f:
    telegram_token = f.readline()

# run bot
bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['vacancy'])
def vacancy(message):
    bot.send_message(message.chat.id, 'Wait a little')

    # take parsed vacancies
    current_date = date.today()
    df = pd.read_parquet(f'./data/vacancies_{current_date}/')

    # make filters
    #####

    text_to_print = ''

    for i in range(1, 10):

        if df["salary"][i - 1] == 'NaN':
            salary = '-'
        else:
            salary = df["salary"][i - 1]

        text_to_print += (
            f'{i}. <b>{str(df["name"][i - 1])}</b> (<a href="{df["link"][i - 1]}">Вакансия на hh.ru</a>)\n'
            f'\t\tSalary: {salary}\n'
            f'\t\tCompany: {str(df["company"][i - 1])}\n'
            f'\t\tCity: {str(df["city"][i - 1])}\n\n')

    bot.send_message(message.chat.id, text=text_to_print, parse_mode='html', disable_web_page_preview=True)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, type the job position you are interested in '
                                      'and the city in russian\nExample: "Data Scientist Москва"')




@bot.message_handler()
def request_handler(message):
    vacancy_name_city = message.text

    user_id = message.from_user.id

    global user_name
    user_name = f'user_{user_id}'

    # Opening JSON file
    json_users = json.load(open('data/users.json'))

    if user_name not in json_users:
        json_users[user_name] = {}

    json_users[user_name]['vacancy'] = vacancy_name_city.split()[:-1]
    json_users[user_name]['city'] = vacancy_name_city.split()[-1]

    out_file = open("data/users.json", "w")
    json.dump(json_users, out_file)

    if type(vacancy_name_city) == str:
        button_0 = types.InlineKeyboardButton('Нет опыта', callback_data='Нет опыта')
        button_1_3 = types.InlineKeyboardButton('От 1 года до 3 лет', callback_data='От 1 года до 3 лет')
        button_3_6 = types.InlineKeyboardButton('От 3 до 6 лет', callback_data='От 3 до 6 лет')
        button_6 = types.InlineKeyboardButton('Более 6 лет', callback_data='Более 6 лет')

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_0)
        keyboard.add(button_1_3)
        keyboard.add(button_3_6)
        keyboard.add(button_6)

        bot.send_message(message.chat.id, text='Select your experience', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    experience = call.data

    # Opening JSON file
    json_users = json.load(open('data/users.json'))

    if user_name not in json_users:
        json_users[user_name] = {}

    json_users[user_name]['experience'] = experience

    out_file = open("data/users.json", "w")
    json.dump(json_users, out_file)


bot.polling(non_stop=True)
