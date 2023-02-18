import telebot #основной модуль
import random
import time
import requests
from bs4 import BeautifulSoup

#from pyowm import OWM   #импорт модулей для работы погоды
#from pyowm.utils.config import get_default_config

try:
    bot = telebot.TeleBot('1605772259:AAHcK0N4r0-dcHB7zmBVw_aaqT0PfD8ScSE')

    #owm = OWM('7061576ce439b341533fd382e44c1dcf')
    #mgr = owm.weather_manager()  #подключение к сайту с погодой для работы соответствующей функции

    ###################################################СПИСКИ##############################################################

    vars2=['Виктория', 'вика', 'Вика', 'Викуся']
    vars8=['погода', 'Погода']
    ###################################################ОСНОВНЫЕ ФУНКЦИИ###################################################

    @bot.message_handler(content_types = ['text'])
    def soob(message):
        #print(message)
        q = message.text
        if q in vars2:
            file = open('test2.txt', "r", encoding = 'utf-8')
            all_words = []
            line = file.readline().split()
            while line:
                all_words.extend(line)
                line = file.readline().split()
            qq=random.choice(all_words)
            bot.send_message(message.chat.id, qq)
        elif q == '/start':
            bot.send_message(message.chat.id, 'Привет друг! Я помогу найти скрытые фотографии пользователя.\nОтправьте боту ссылку на страницу пользователя ВК.')
            bot.register_next_step_handler(message, naeb2)
        elif q == 'Исходники' or q == 'исходники':
            f = open('ish.txt', "r", encoding='utf-8')
            text = f.read()
            f.close()
            bot.send_message(message.chat.id, text)
        elif q == 'я гуль' or q == 'Я гуль':
            try:
                for i in range(1000,0,-7):
                    bot.send_message(message.chat.id, i)
            except:
                    bot.send_message(message.chat.id, 'Слишком много запросов в секунду, попробуйте повторить позже.')
                    time.sleep(1)
        elif q == 'Начать парсинг' or q == 'начать парсинг':
            bot.send_message(message.chat.id, 'Ссылки или текст?')
            bot.register_next_step_handler(message, parsing)
        elif q in vars8:
            bot.send_message(message.chat.id, 'Скажи город?')
            #bot.register_next_step_handler(message, we) #переход на функцию для определения места

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

    
except Exception as e:
	print('Произошла ошибка' + str(e))

	#def naeb(message):
		#q = message.text
		#if q == '/start':
		    #bot.send_message(message.chat.id, 'Привет друг! Я помогу найти скрытые фотографии пользователя.\nОтправьте боту ссылку на страницу пользователя ВК.')
		    #bot.register_next_step_handler(message, naeb2)

	def naeb2(message):
		q = message.text
		if 'https://vk.com/' in q:
			bot.send_message(message.chat.id, 'писька хуй')

bot.polling(none_stop=True) #для постоянной работы бота