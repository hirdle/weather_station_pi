# -*- coding: utf-8 -*-

import schedule
import time
import telebot
import requests
from telebot import types
from multiprocessing.context import Process
import Adafruit_DHT
import json

filename = 'data.json'
data = None

with open(filename, "r") as file:
    data = json.load(file)

def send():
    bot.send_message(941935092, "effefef")

def send_schedules_messages():
    with open(filename, "r") as file:
        data = json.load(file)
    for i in data[0]['times']:
        schedule.every().day.at(i).do(send)
send_schedules_messages()
def show_time():
    message_data = ""
    for i in data[0]['times']:
        message_data += (i+"\n")
    return message_data

def dump_json():
    with open(filename, "w") as file:
        json.dump(data, file)
    send_schedules_messages()


def delete_time(time):
    for i in range(len(data[0]['times'])):
        if data[0]['times'][i] == time:
            data[0]['times'].pop(i)

    dump_json()

def add_time(time):
    element_is = False
    for i in range(len(data[0]['times'])):
        if data[0]['times'][i] == time:
            element_is = True

    if(element_is == False):
        data[0]['times'].append(time)
    dump_json()
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

TOKEN = '5194527013:AAGKZcXHcub8E4UJM0U_HG9CxSUPDAeGmXU'
bot = telebot.TeleBot(TOKEN)


import Adafruit_BMP.BMP085 as BMP085
bmp180Sensor = BMP085.BMP085()

tel_id_1 = "941935092"

weather_text = """
Информация о погоде {0}:\n
Температура - {1}C
Влажность - {2}%
Давление - {3} мм ртуртного столба
Высота над уровнем моря: {4} м
Ощущается как - {5}C
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

def add_times(result_time):
    markup = return_menu()
    add_time(result_time.text)
    bot.send_message(result_time.chat.id, "*Время {0} успешно добавлено*".format(result_time.text), parse_mode= 'Markdown', reply_markup=markup)

def delete_times(result_time):
    if(result_time.text != "Назад в меню"):
        markup = return_menu()
        delete_time(result_time.text)
        bot.send_message(result_time.chat.id, "*Время {0} успешно удалено*".format(result_time.text), parse_mode= 'Markdown', reply_markup=markup)

def return_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Назад в меню")
    markup.add(item1)
    return markup

def start_function(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Погода в данный момент")
    item2 = types.KeyboardButton("Прогноз погоды")
    item3 = types.KeyboardButton("Настройка оповещения")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.chat.id, 'Выберите функцию:', reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message, res=False):
    start_function(message)
    # bot.edit_message_text(message.chat.id, message.id, inline_message_id, text, reply_markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):
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
        print('lox')
        weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather", params=api_weather_data).json()

        tempBMP = round(bmp180Sensor.read_temperature(), 1)
        presBMP = round(bmp180Sensor.read_pressure()/100*0.7501, 1)
        altBMP =  round(bmp180Sensor.read_altitude(),1)

        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None:
            bot.send_message(message.chat.id, weather_text.format(city_ru, tempBMP, humidity, presBMP, altBMP, weather_data['main']['feels_like']))
        else:
            bot.send_message(message.chat.id, weather_text.format(city_ru, tempBMP, weather_data['main']['humidity'], presBMP, altBMP, weather_data['main']['feels_like']))
    elif message.text.strip() == 'Прогноз на 1 день':
        bot.send_message(message.chat.id, get_forecast_data(2), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на 3 дня':
        bot.send_message(message.chat.id, get_forecast_data(4), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на сегодня':
        bot.send_message(message.chat.id, get_forecast_data(1), parse_mode= 'Markdown')
    elif message.text.strip() == 'Прогноз на 5 дней':
        bot.send_message(message.chat.id, get_forecast_data(5), parse_mode= 'Markdown')

    elif message.text.strip() == 'Настройка оповещения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Показать все время оповещения")
        item2 = types.KeyboardButton("Добавить оповещение")
        item3 = types.KeyboardButton("Удалить оповещение")
        item4 = types.KeyboardButton("Назад в меню")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, 'Выберите функцию:', reply_markup=markup)

    elif message.text.strip() == 'Показать все время оповещения':
        message_data = show_time()
        bot.send_message(message.chat.id, message_data)

    elif message.text.strip() == 'Назад в меню':
        start_function(message)

    elif message.text.strip() == 'Добавить оповещение':
        markup = return_menu()
        send = bot.send_message(message.chat.id, 'Напишите время, которое хотите добавить', reply_markup=markup)
        bot.register_next_step_handler(send, add_times)
    elif message.text.strip() == 'Удалить оповещение':
        message_data = show_time()
        markup = return_menu()
        send = bot.send_message(message.chat.id, 'Напишите время, которое хотите удалить: \n'+ message_data, reply_markup=markup)
        bot.register_next_step_handler(send, delete_times)


class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)
 
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()
 

# bot.polling(none_stop=True)

 
if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass