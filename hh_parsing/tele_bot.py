import telebot
import pandas as pd
from config import telegram_token

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Hello, write the job position you are interested in')


@bot.message_handler(commands=['vacancy'])
def main(message):
    bot.send_message(message.chat.id, 'Wait a little')

    df = pd.read_csv('data/hh_data.csv')
    text_to_print = 'Todays vacancies'

    bot.send_message(message.chat.id, '<a href="http://www.example.com/">text</a>', parse_mode='html')


@bot.message_handler()
def main(message):
    vacancy_name = message.text.lower()

    with open("config.py", "a") as f:
        f.write(f"vacancy_name = \'{vacancy_name}\'")

bot.polling(non_stop=True)