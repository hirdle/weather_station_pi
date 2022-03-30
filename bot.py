# -*- coding: utf-8 -*-

from unittest import result
import schedule
import time
import telebot
import requests
from telebot import types
from multiprocessing.context import Process

TOKEN = '5194527013:AAGKZcXHcub8E4UJM0U_HG9CxSUPDAeGmXU'
bot = telebot.TeleBot(TOKEN)

tel_id_1 = "941935092"

weather_text = """
Информация о погоде в городе {0}:\n
Температура - {1}C
Влажность - {2}%
Давление - {3}Гп
Ощущается как - {4}C
Все. конец.
"""
city_ru = 'Пенза'
city_en = 'Penza'
API_key_weather = "3ba9c0e9246cf9ee76413878ea521077"

api_weather_data = {'q': city_en, 'units': 'metric', 'APPID': API_key_weather, 'lang': 'ru'}

def get_forecast_data(days):
    try:
        result_forecast = ""

        res = requests.get("http://api.openweathermap.org/data/2.5/forecast", api_weather_data)
        data = res.json()['list']

        temp_list = []
        result_list = []
        for i in data:
            if(i['dt_txt'][11:] != '00:00:00'):
                temp_list.append(i)
            else:
                temp_list.append(i)
                result_list.append(temp_list)
                temp_list = []
        start_index = 0
        if(days != 1): start_index = 1
        for i in range(start_index, days):
            result_forecast += "\n*Погода на " + result_list[i][0]['dt_txt'][:10] + '*\n'
            for i in result_list[i]:
                result_forecast += i['dt_txt'][11:16] + ' ' + '{0:+3.0f}'.format(i['main']['temp']) + ' ' + i['weather'][0]['description']  + '\n' 
        return result_forecast
    except:
        pass
def start_function(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Погода в данный момент")
    item2 = types.KeyboardButton("Прогноз погоды")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Выберите функцию:', reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message, res=False):
    start_function(message)
    # bot.edit_message_text(message.chat.id, message.id, inline_message_id, text, reply_markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    answer = ""
    if message.text.strip() == 'Прогноз погоды':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item5 = types.KeyboardButton("Прогноз на сегодня")
        item1 = types.KeyboardButton("Прогноз на 1 день")
        item2 = types.KeyboardButton("Прогноз на 3 дня")
        item3 = types.KeyboardButton("Прогноз на 5 дней")
        item4 = types.KeyboardButton("Назад в меню")
        markup.add(item5)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, 'Выберите прогноз:', reply_markup=markup)
    elif message.text.strip() == 'Погода в данный момент':
        weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather", params=api_weather_data).json()
        bot.send_message(message.chat.id, weather_text.format(city_ru, weather_data['main']['temp'], weather_data['main']['humidity'], weather_data['main']['pressure'], weather_data['main']['feels_like']))
    elif message.text.strip() == 'Прогноз на 1 день':
        bot.send_message(message.chat.id, get_forecast_data(2), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на 3 дня':
        bot.send_message(message.chat.id, get_forecast_data(4), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на сегодня':
        bot.send_message(message.chat.id, get_forecast_data(1), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на 5 дней':
        bot.send_message(message.chat.id, get_forecast_data(5), parse_mode= 'Markdown')

    elif message.text.strip() == 'Назад в меню':
        start_function(message)

    # bot.send_message(message.chat.id, answer)


class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)
 
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()
 
 
if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass