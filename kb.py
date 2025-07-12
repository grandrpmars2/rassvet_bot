# Keyboards

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton



#beginning_keyboard = ReplyKeyboardMarkup(keyboard=beginning_keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)
#beginning_keyboard.row(beginning_keyboard_buttons[0, 1]).add()

# beginning_keyboard
def beginning_keyboard():
	beginning_keyboard_buttons = [
		[types.KeyboardButton(text="Общественная приемная"), types.KeyboardButton(text="Стать сторонником")],
		[types.KeyboardButton(text="Связаться по другому вопросу")]
	]
	beginning_keyboard = ReplyKeyboardMarkup(keyboard=beginning_keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)

	return beginning_keyboard

def back_to_beginning_keybiard():
	beginning_keyboard_buttons = [
		[types.KeyboardButton(text="Отменить отправку")]
	]
	beginning_keyboard = ReplyKeyboardMarkup(keyboard=beginning_keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)

	return beginning_keyboard

# admin list keyboard
def admin_list_button(admin_list):
	admin_buttons = []
	for admin in admin_list:
		cb_string = "delete " + str(admin)
		admin_buttons.append([types.InlineKeyboardButton(text=f'{admin} ❌', callback_data=cb_string)])

	admins_keyboard = types.InlineKeyboardMarkup(inline_keyboard=admin_buttons)

	return admins_keyboard


# activities keyboard
# activity1 = 0
# activity2 = 0
# activity3 = 0
# activity4 = 0
# activity5 = 0
# activity6 = 0
# activity7 = 0

def activities_keyboard(state_data):
	buttons = []

	if state_data['activity1'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ Политической деятельностью, участвовать в выборах', callback_data='activity1')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ Политической деятельностью, участвовать в выборах', callback_data='activity1')])
	
	if state_data['activity2'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ СМИ и медиа', callback_data='activity2')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ СМИ и медиа', callback_data='activity2')])

	if state_data['activity3'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ Проектами по экологии и зоозащите', callback_data='activity3')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ Проектами по экологии и зоозащите', callback_data='activity3')])

	if state_data['activity4'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ Работой, связанной с урбанистикой', callback_data='activity4')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ Работой, связанной с урбанистикой', callback_data='activity4')])

	if state_data['activity5'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ Социальной работой', callback_data='activity5')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ Социальной работой', callback_data='activity5')])

	if state_data['activity6'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ Хочу развивать свой проект или направление', callback_data='activity6')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ Хочу развивать свой проект или направление', callback_data='activity6')])

	if state_data['activity7'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ Пока не готов(а) ответить, хочу подробнее все изучить', callback_data='activity7')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ Пока не готов(а) ответить, хочу подробнее все изучить', callback_data='activity7')])

	if state_data['activity8'] == 1:
		buttons.append([InlineKeyboardButton(text='✅ Другой вариант (напишу)', callback_data='activity8')])
	else:
		buttons.append([InlineKeyboardButton(text='⬜️ Другой вариант (напишу)', callback_data='activity8')])

	buttons.append([InlineKeyboardButton(text='Далее →', callback_data='next')])
	

	return InlineKeyboardMarkup(inline_keyboard=buttons)

def over_eighteen_markup():
	buttons = []

	buttons.append([InlineKeyboardButton(text='Да', callback_data='eighteen_yes')])
	buttons.append([InlineKeyboardButton(text='Нет', callback_data='eighteen_no')])

	return InlineKeyboardMarkup(inline_keyboard=buttons)


def future_member_markup():
	buttons = []

	buttons.append([InlineKeyboardButton(text='Хочу вступить в партию', callback_data='future_member')])
	buttons.append([InlineKeyboardButton(text='Хочу остаться сторонником', callback_data='future_follower')])

	return InlineKeyboardMarkup(inline_keyboard=buttons)

def soglasie_markup():
	buttons = []

	buttons.append([InlineKeyboardButton(text='Даю согласие', callback_data='soglasie_yes')])
	buttons.append([InlineKeyboardButton(text='Не даю, вернуться в начало', callback_data='soglasie_no')])

	return InlineKeyboardMarkup(inline_keyboard=buttons)

def send_anketa():
	buttons = []

	buttons.append([InlineKeyboardButton(text='Отправить анкету', callback_data='anketa_send')])
	buttons.append([InlineKeyboardButton(text='Отменить отправку', callback_data='anketa_start')])

	return InlineKeyboardMarkup(row_width=2, inline_keyboard=buttons)