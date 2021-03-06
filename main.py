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

del_list = []

for i in base.Sqlopen().returner('admins'):
	del_list.append(i)
count = 0
for i in base.Sqlopen().returner('chanel'):
	try:
		bot.delete_message(i, del_list[count])
		count += 1
	except:
		continue

	time.sleep(1)
for i in base.Sqlopen().returner('admins'):
	try:
		base.Sqlopen().deleter('admins', 'id', i[0])
	except:
		continue



def sender():
	time.sleep(5)
	while 1:
		del_list = []
		message_dict = {}
		for i in base.Sqlopen().returner('chanel'):
			for x in base.Sqlopen().returner('data'):
				try:
					r = bot.send_message(chat_id = i[0], text = f"<b>Заказы АВРОРА КРЫМ</b>\n{x[0]}\n<b>Взять заказ Жми ссылку</b>" + ' ' + '<a href="https://t.me/Elena_Mercedes_Vito">Elena_Mercedes_Vito</a>', parse_mode='HTML', disable_web_page_preview=True)
					base.Sqlopen().add_chanell('admins', r.message_id)
					message_dict[r.message_id] = r.chat.id
					time.sleep(1)
				except:
					continue
		for i in range(sleep_time):
			global crutch
			if crutch == True:
				break
			else:
				time.sleep(1)
		crutch = False
		time.sleep(1)
		for i in message_dict.items():
			try:
				bot.delete_message(i[1], i[0])
				base.Sqlopen().deleter('admins', 'id', i[0])
				time.sleep(1)
			except:
				continue
		time.sleep(2)
rT = threading.Thread(target = sender)
rT.start()

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
	bot.send_message(call.message.chat.id, 'Введите ID каналов в которые нужно переслать сообщение', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))	
	bot.register_next_step_handler(call.message, confirm_chanell)


def confirm_chanell(message):    
	global crutch
	crutch = True
	base.Sqlopen().add_chanell('chanel', message.text)
	bot.send_message(message.chat.id, 'Канал успешно добавлен', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
	time.sleep(1)


#################################################################################
#Add message function
#################################################################################
@bot.callback_query_handler(func=lambda call: True and call.data == 'send_message')
def add_text(call):
	time.sleep(1)
	bot.send_message(call.message.chat.id, 'Отправьте сообщение', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
	bot.register_next_step_handler(call.message, confirm_add_text)

def confirm_add_text(message): 
	global crutch
	crutch = True
	base.Sqlopen().add_data('data', message.text)
	bot.send_message(message.chat.id, 'Сообщение успешно добавлено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
	time.sleep(2)




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
		bot.send_message(call.message.chat.id, answer, reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
		bot.register_next_step_handler(call.message, confirm_del_text)
	else:
		bot.send_message(call.message.chat.id, "Список пуст", reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))

def confirm_del_text(message): 
	global crutch
	crutch = True
	base.Sqlopen().deleter('data', 'message', base.Sqlopen().returner('data')[int(message.text) - 1][0])
	bot.send_message(message.chat.id, 'Сообщение успешно удалено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
	time.sleep(2)

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
		bot.send_message(call.message.chat.id, answer, reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
		bot.register_next_step_handler(call.message, confirm_del_link)
	else:
		time.sleep(1)
		bot.send_message(call.message.chat.id, "Список пуст", reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))		
def confirm_del_link(message): 
	global crutch
	crutch = True
	base.Sqlopen().deleter('chanel', 'chanels_id', base.Sqlopen().returner('chanel')[int(message.text) - 1][0])
	bot.send_message(message.chat.id, 'Сообщение успешно удалено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))
	time.sleep(2)


###########################################################################################



@bot.callback_query_handler(func=lambda call: True and call.data == 'cancel')
def cancel(call):
	time.sleep(1)
	bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Админ панель', reply_markup=create_inlineKeyboard({"Добавить канал":"chanel",
																										  											 "Добавить сообщение":"send_message",
																																					 "Убрать канал":"kill_chanel",
																																					 "Убрать сообщение":"kill_message"},
																																					 row = 2))



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
