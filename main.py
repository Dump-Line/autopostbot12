import telebot
import config
import sqlite3
import base
import time
from datetime import datetime, timedelta
from text import *
import threading
from flask import Flask, request
import os
import sys

global crutch
crutch = False

HEROKU_LINK = "https://autopost12.herokuapp.com/"
TOKEN = config.token
bot = telebot.TeleBot(config.token)
server = Flask(__name__)

def split_list(arr, wanted_parts=1):
     arrs = []
     while len(arr) > wanted_parts:
         pice = arr[:wanted_parts]
         arrs.append(pice)
         arr = arr[wanted_parts:]
     arrs.append(arr)
     return arrs

def create_inlineKeyboard(key,row=0):
	keyboard = telebot.types.InlineKeyboardMarkup()
 
	if row == 0:
		for i in key:
			c = key.get(i)
			keyboard.add(telebot.types.InlineKeyboardButton(text=i, callback_data=c))
	else:
		key_list = []
	   
		for i in key:
			c = key.get(i)
			key_list.append(telebot.types.InlineKeyboardButton(text=i, callback_data=c))       
	   
		for i in split_list(key_list,row):
			keyboard.add(*[name for name in i])
 
	return keyboard








@bot.message_handler(commands=['panel'])
def check_status(message):
	if message.chat.type != 'private':
		return ''
	for i in admin_id:
		print(i)
		print(message.chat.id)
		if str(message.chat.id) == i:
			bot.send_message(message.chat.id, 'Админ панель', reply_markup=create_inlineKeyboard({"Добавить канал":"chanel",
																							      "Добавить сообщение":"send_message",
																							      "Убрать канал":"kill_chanel",
																							      "Убрать сообщение":"kill_message"}, 2))
################################################################################
# Add chanel function
################################################################################
@bot.callback_query_handler(func=lambda call: True and call.data == 'chanel')
def add_chanell(call):
	bot.send_message(call.message.chat.id, 'Введите ID каналов в которые нужно переслать сообщение')	
	bot.register_next_step_handler(call.message, confirm_chanell)

def confirm_chanell(message):    
	for i in base.Sqlopen().returner('data'):
		if message.text == i[0]:
			bot.send_message(message.chat.id, 'Канал уже в списке', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
			return ''
	global crutch
	crutch = True
	base.Sqlopen().add_chanell('chanel', message.text)
	bot.send_message(message.chat.id, 'Канал успешно добавлен', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))


#################################################################################
#Add message function
#################################################################################
@bot.callback_query_handler(func=lambda call: True and call.data == 'send_message')
def add_text(call):
	bot.send_message(call.message.chat.id, 'Отправьте сообщение')
	bot.register_next_step_handler(call.message, confirm_add_text)

def confirm_add_text(message): 
	global crutch
	crutch = True
	base.Sqlopen().add_data('data', message.text)
	bot.send_message(message.chat.id, 'Сообщение успешно добавлено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))




##################################################################################
# del text function
######################################################################################

@bot.callback_query_handler(func=lambda call: True and call.data == 'kill_message')
def del_text(call):
	count = 1
	answer = ''
	if len(base.Sqlopen().returner('data')) != 0:
		for i in base.Sqlopen().returner('data'):
			answer += f'{str(count)}.{str(i[0])} \n'
			count += 1
		answer += 'Введите номер сообщения которое нужно удалить'
		bot.send_message(call.message.chat.id, answer)
		bot.register_next_step_handler(call.message, confirm_del_text)
	else:
		bot.send_message(call.message.chat.id, "Список пуст", reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))

def confirm_del_text(message): 
	global crutch
	crutch = True
	base.Sqlopen().deleter('data', 'message', base.Sqlopen().returner('data')[int(message.text) - 1][0])
	bot.send_message(message.chat.id, 'Сообщение успешно удалено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))

######################################################################################
# del chanel function
######################################################################################

@bot.callback_query_handler(func=lambda call: True and call.data == 'kill_chanel')
def del_link(call):
	count = 1
	answer = ''
	if len(base.Sqlopen().returner('chanel')) != 0:
		for i in base.Sqlopen().returner('chanel'):
			answer += f'{str(count)}.{str(i[0])} \n'
			count += 1
		answer += 'Введите номер сообщения которое нужно удалить'
		bot.send_message(call.message.chat.id, answer)
		bot.register_next_step_handler(call.message, confirm_del_link)
	else:
		bot.send_message(call.message.chat.id, "Список пуст", reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))		
def confirm_del_link(message): 
	global crutch
	crutch = True
	base.Sqlopen().deleter('chanel', 'chanels_id', base.Sqlopen().returner('chanel')[int(message.text) - 1][0])
	bot.send_message(message.chat.id, 'Сообщение успешно удалено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))


###########################################################################################



@bot.callback_query_handler(func=lambda call: True and call.data == 'cancel')
def cancel(call):
	bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Админ панель', reply_markup=create_inlineKeyboard({"Добавить канал":"chanel",
																										  											 "Добавить сообщение":"send_message",
																																					 "Убрать канал":"kill_chanel",
																																					 "Убрать сообщение":"kill_message"},
																																					 row = 2))

def send():
	while 1:
		message_dict = {}
		for i in base.Sqlopen().returner('chanel'):
			for x in base.Sqlopen().returner('data'):
				r = bot.send_message(i[0], f"*Заказы АВРОРА КРЫМ*\n {x[0]} \n*Взять заказ Жми ссылку* {'@Elena_Mercedes_Vito'}", parse_mode= 'Markdown')
				message_dict[r.message_id] = r.chat.id
				time.sleep(1.6)
		for i in range(sleep_time):
			global crutch
			if crutch == True:
				crutch = False
				break
			else:
				time.sleep(1)
		for i in message_dict.items():
			bot.delete_message(i[1], i[0])
			time.sleep(8)
rT = threading.Thread(target = send)
rT.start()

#######################################
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
  bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
  return "!", 200


@server.route("/")
def webhook():
  bot.remove_webhook()
  bot.set_webhook(url=HEROKU_LINK + TOKEN)
  return "!", 200


# Получаем новые сообщения
if __name__ == "__main__":
  server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))) 
  print("START")
