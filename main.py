import telebot
import config
import sqlite3
import base
import time
from datetime import datetime, timedelta
from text import *
import threading

bot = telebot.TeleBot(config.token)



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
	check_list = []	
	for i in base.Sqlopen('sender.db').returner('admins'):
		check_list.append(list(i)[0])
	if str(message.from_user.id) != admin_id:
		return ''
	if message.chat.type != 'private':
		if message.from_user.id not in check_list:
			return ''
	else:
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
	base.Sqlopen('sender.db').add_chanell('chanel', message.text)
	bot.send_message(message.chat.id, 'Канал успешно добавлен', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))








#################################################################################
#Add message function
#################################################################################
@bot.callback_query_handler(func=lambda call: True and call.data == 'send_message')
def add_text(call):
	bot.send_message(call.message.chat.id, 'Отправьте сообщение')
	bot.register_next_step_handler(call.message, confirm_add_text)

def confirm_add_text(message): 
	base.Sqlopen('sender.db').add_data('data', message.text)
	bot.send_message(message.chat.id, 'Сообщение успешно добавлено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))




##################################################################################
# del text function
######################################################################################

@bot.callback_query_handler(func=lambda call: True and call.data == 'kill_message')
def del_text(call):
	count = 1
	answer = ''
	if len(base.Sqlopen('sender.db').returner('data')) != 0:
		for i in base.Sqlopen('sender.db').returner('data'):
			answer += f'{str(count)}.{str(i[0])} \n'
			count += 1
		answer += 'Введите номер сообщения которое нужно удалить'
		bot.send_message(call.message.chat.id, answer)
		bot.register_next_step_handler(call.message, confirm_del_text)
	else:
		bot.send_message(call.message.chat.id, "Список пуст", reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))

def confirm_del_text(message): 
	base.Sqlopen('sender.db').deleter('data', 'message', base.Sqlopen('sender.db').returner('data')[int(message.text) - 1][0])
	bot.send_message(message.chat.id, 'Сообщение успешно удалено', reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))

######################################################################################
# del chanel function
######################################################################################

@bot.callback_query_handler(func=lambda call: True and call.data == 'kill_chanel')
def del_link(call):
	count = 1
	answer = ''
	if len(base.Sqlopen('sender.db').returner('chanel')) != 0:
		for i in base.Sqlopen('sender.db').returner('chanel'):
			answer += f'{str(count)}.{str(i[0])} \n'
			count += 1
		answer += 'Введите номер сообщения которое нужно удалить'
		bot.send_message(call.message.chat.id, answer)
		bot.register_next_step_handler(call.message, confirm_del_link)
	else:
		bot.send_message(call.message.chat.id, "Список пуст", reply_markup=create_inlineKeyboard({"Вернуться в Админ панель":"cancel"}))		
def confirm_del_link(message): 
	base.Sqlopen('sender.db').deleter('chanel', 'chanels_id', base.Sqlopen('sender.db').returner('chanel')[int(message.text) - 1][0])
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
		for i in base.Sqlopen('sender.db').returner('chanel'):
			for x in base.Sqlopen('sender.db').returner('data'):
				message = "Заказы Аврора:" + '\n' + x[0] + '\n' + f'По заказам писать  - Такси Аврора {url}'
				bot.send_message(i[0], message)
		time.sleep(sleep_time)

rT = threading.Thread(target = send)
rT.start()


if __name__ == '__main__':
	bot.polling(none_stop=True)
