# Отправка обращений в админ-группу

from config import ADMIN_GROUP_CHAT_ID


async def new_message_to_admin_group(message, bot):
	msg = f"<b>Поступило сообщение о проблеме!</b>\n\n{message.text}\n\nОт: <b>{message.from_user.username} ({message.from_user.id})</b> \nДата и время: <i>{message.date.date()} {message.date.time()}</i>"

	await bot.send_message(ADMIN_GROUP_CHAT_ID, msg)

async def new_anketa_to_admin_group(message, bot):
	await bot.send_message(ADMIN_GROUP_CHAT_ID, 'Поступила новая заявка в сторонники!')
	await bot.send_message(ADMIN_GROUP_CHAT_ID, message)

async def new_connect_to_admin_group(message, bot):
	msg = f"<b>Поступило обращение из раздела 'Связаться по другому вопросу'!</b>\n\n{message.text}\n\nОт: <b>{message.from_user.username} ({message.from_user.id})</b> \nДата и время: <i>{message.date.date()} {message.date.time()}</i>"

	await bot.send_message(ADMIN_GROUP_CHAT_ID, msg)


'''
email = 'asdasd@gmail.com'
activity1 = 0
activity2 = 1
activity3 = 1
activity4 = 1
activity5 = 1
activity6 = 1
activity7 = 1
activity8 = 'asdasdasdad'
fio = 'asdadad ads asd'
tg = '@asdasda'
phone_number = '13123123'
eighteen = 'eighteen_yes' / 'eighteen_no'
living_perm_krai = 'living_yes_1' / 'living_yes_2' / 'living_no'
town = 'kumis'
future = 'future_member' / 'future_follower'
social_media = 'asda'
additional_info = 'adfdf'

'''
async def format_anketa (state_data):
	print(state_data['eighteen'])
	if state_data['eighteen'] == 'eighteen_yes':
		age_text = 'старше 18 лет'
	elif state_data['eighteen'] == 'eighteen_no':
		age_text = 'младше 18 лет'

	if state_data['living_perm_krai'] == 'living_yes_1':
		living_text = 'постоянно живу, есть регистрация'
	elif state_data['living_perm_krai'] == 'living_yes_2':
		living_text = 'преимущественно проживаю, постоянной регистрации нет'
	elif state_data['living_perm_krai'] == 'living_no':
		living_text = 'не проживаю'

	activities_text = ''
	if state_data['activity1'] == 1:
		activities_text += f'- Политической деятельностью, участвовать в выборах\n'
	if state_data['activity2'] == 1:
		activities_text += f'- СМИ и медиа\n'
	if state_data['activity3'] == 1:
		activities_text += f'- Проектами по экологии и зоозащите\n'
	if state_data['activity4'] == 1:
		activities_text += f'- Работой, связанной с урбанистикой\n'
	if state_data['activity5'] == 1:
		activities_text += f'- Социальной работой\n'
	if state_data['activity6'] == 1:
		activities_text += f'- Развитием своего проекта или направления\n'
	if state_data['activity7'] == 1:
		activities_text += f'- Пока не готов(а) ответить, хочу подробнее все изучить\n'

	if state_data['activity8'] != 0:
		activities_text += f"- {state_data['activity8']}\n"
	else:
		activities_text += '\n'

	if state_data['future'] == 'future_member':
		future_text = 'членом партии'
	elif state_data['future'] == 'future_follower':
		future_text = 'сторонником'

	message_text = f"<b>{state_data['fio']}</b>\nВозраст: {age_text}\n\nТелеграм: {state_data['tg']}\nДругие социальные сети: {state_data['social_media']}\nНомер телефона: {state_data['phone_number']}\n\nПроживание в Пермском крае: {living_text}\nГород: {state_data['town']}\n\nГотов заниматься:\n{activities_text}\n Хочу стать {future_text}\n\nДополнительная информация: {state_data['additional_info']}"
	return message_text