import telebot #основной модуль
import random
import time
import requests
from bs4 import BeautifulSoup

from pyowm import OWM   #импорт модулей для работы погоды
from pyowm.utils.config import get_default_config

try:
	bot = telebot.TeleBot('1605772259:AAHcK0N4r0-dcHB7zmBVw_aaqT0PfD8ScSE')

	owm = OWM('7061576ce439b341533fd382e44c1dcf')
	mgr = owm.weather_manager()  #подключение к сайту с погодой для работы соответствующей функции

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
			bot.register_next_step_handler(message, we) #переход на функцию для определения места

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

	def we(message):
		try:                    #функция отправки погоды в определенном городе
			global place
			place = message.text
			if place == 'город':
				bot.send_message(message.chat.id, 'дурак?')
			else:
				config_dict = get_default_config()
				config_dict['language'] = 'ru'  #выбор языка
				observation = mgr.weather_at_place(place) #основа всего
				w = observation.weather
				temp = w.temperature('celsius')['temp'] # средняя температура
				temp2 = w.temperature('celsius')['temp_min'] # минимальная
				temp3 = w.temperature('celsius')['temp_max'] # максимальная, как неудивительно
				wind = w.wind()['speed'] # значение ветра
				wind2 = w.humidity # влажность
				wind3 = w.rain # значение дождя
				ans='В городе ' + place + ' сейчас ' +  w.detailed_status + '\n'
				ans+='средняя температура ' + str(temp) + ' градусов цельсия, минимальная температура ' + str(temp2) + ' градусов цельсия, максимальная температура ' + str(temp3) + ' градусов цельсия'+ '\n'
				ans+='скорость ветра ужас, ' + str(wind) + ' метров в секунду' +'\n'
				ans+='влажность ' + str(wind2) + '\n'
				ans+=' дождь, ну, вот значение ' + str(wind3) + '\n'
				if temp>=30:
				    ans+='жарко сегодня...\n'
				elif temp<=-30:
				    ans+='холодно сегодня...'
				elif temp >-30 and temp <=-15:
				    ans+='прохладенько сегодня...'
				elif temp <=0 and temp >-15:
				    ans+='холодно...'
				elif temp >=0 and temp <20:
				    ans+='ну шорты надеть можно, я думаю'
				elif temp >=20 and temp <30:
				    ans+='все, можно и на шашлычки))'
				bot.send_message(message.chat.id, ans)
		except Exception as e:
			bot.send_message(message.chat.id, 'Либо нету такого города, либо проверьте написание команды, код ошибки: ' + str(e))
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

bot.polling(none_stop=True) #для постоянной работы бот