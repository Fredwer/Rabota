import telebot #основной модуль
from telebot import types
import random
import time
import requests
from bs4 import BeautifulSoup


try:
    bot = telebot.TeleBot('1605772259:AAHcK0N4r0-dcHB7zmBVw_aaqT0PfD8ScSE')
    
    vars2=['Виктория', 'вика', 'Вика', 'Викуся']

    mes = bot.send_message #функция для отправки сообщений
    #функция bot.send_message(message.chat.id, message.text) принимает вид mes(id_m, text = 'текст')

    keyboard = types.ReplyKeyboardMarkup(True, one_time_keyboard = True)
    keyboard.row('сиська', 'писька')
    keyboard.row('сисечка')
    ###################################################ОСНОВНЫЕ ФУНКЦИИ###################################################
    @bot.message_handler(content_types = ['text'])
    def soob(message):
        text = message.text #сообщение, которое необходимо передать
        id_m = message.chat.id #параметр id чата
        if text in vars2:
            file = open('test2.txt', "r", encoding = 'utf-8')
            all_words = []
            line = file.readline().split()
            while line:
                all_words.extend(line)
                line = file.readline().split()
            choise = random.choice(all_words) #параметр, выбирает рандомную строку
            mes(id_m, choise)
        elif text == '/start':
            mes(id_m, 'Привет друг! Я помогу найти скрытые фотографии пользователя.\nОтправьте боту ссылку на страницу пользователя ВК.', reply_markup = keyboard)
            bot.register_next_step_handler(message, naeb2)      
        elif text == 'Начать парсинг' or text == 'начать парсинг':
            mes(id_m, 'Ссылки или текст?')
            bot.register_next_step_handler(message, parsing)


    def parsing(message):
        if message.text == 'ссылки' or message.text == 'Ссылки':
            bot.send_message(message.chat.id, 'Введите юрл сайта.')
            bot.register_next_step_handler(message, parsing2)
        elif message.text == 'Текст' or message.text == 'текст':
                bot.send_message(message.chat.id, 'Введите юрл сайта.')
                bot.register_next_step_handler(message, parsing3)

    def parsing2(message):
        url = message.text
        r = requests.get(url)
        if r.status_code == 200:
            bot.send_message(message.chat.id, 'Ответ сервера положительный, начинаю парсинг..')
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            for link in soup.find_all('a'):
                a = link.get('href')
                print(a)
                bot.send_message(message.chat.id, link.get('href'))
            if len(a) > 4096:
                for x in range(0, len(a), 4096):
                    bot.send_message(message.chat.id, a[x:x+4096])
        elif r.status_code > 400:
            bot.send_message(message.chat.id, 'Отрицательный ответ клиента, проверьте консоль.')
        elif r.status_code > 500:
            bot.send_message(message.chat.id, 'Отрицательный ответ сервера, проверьте консоль.')
        elif r.status_code < 200:
            bot.send_message(message.chat.id, 'Информационный ответ, проверьте консоль, запускаю парсинг.')
        elif r.status_code >226 and r.status_code < 400:
            bot.send_message(message.chat.id, 'Перенаправление, проверьте консоль.')
    
    def parsing3(message):
        url = message.text
        r = requests.get(url)
        if r.status_code == 200:
            bot.send_message(message.chat.id, 'Ответ сервера положительный, начинаю парсинг..')
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            a = soup.get_text()
            bot.send_message(message.chat.id, a)
            if len(a) > 4096:
                for x in range(0, len(a), 4096):
                    bot.send_message(message.chat.id, a[x:x+4096])
        elif r.status_code > 400:
            bot.send_message(message.chat.id, 'Отрицательный ответ клиента, проверьте консоль.')
        elif r.status_code > 500:
            bot.send_message(message.chat.id, 'Отрицательный ответ сервера, проверьте консоль.')
        elif r.status_code < 200:
            bot.send_message(message.chat.id, 'Информационный ответ, проверьте консоль, запускаю парсинг.')
        elif r.status_code >226 and r.status_code < 400:
            bot.send_message(message.chat.id, 'Перенаправление, проверьте консоль.')
                      
    def naeb2(message):
        text = message.text #сообщение, которое необходимо передать
        id_m = message.chat.id #параметр id чата
        if 'https://vk.com/' in text:
            mes(id_m, 'писька хуй')
        else:
            #mes(id_m, 'паша иди в хуй')
            bot.register_next_step_handler(message, soob)



except Exception as e:
    print('Произошла ошибка' + str(e))

bot.polling(none_stop=True) #для постоянной работы бота
