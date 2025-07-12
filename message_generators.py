# Отправка обращений в админ-группу

from config import ADMIN_GROUP_CHAT_ID


async def new_message_to_admin_group(message, bot, state=None):
	if state: #если обращение новое, а не сообщение по старому обращению
		msg = f"<b>Поступило сообщение о проблеме!</b>\n\nКак можно обращаться: {state['problem_naming']}\nМесто: <i>{state['problem_place']}</i>\nОписание проблемы: {state['problem_description']}\n\nОт: <b>{message.from_user.username} ({message.from_user.id})</b> \nДата и время: <i>{message.date.date()} {message.date.time()}</i>"
	else:
		if message.photo:
			msg = f"От: <b>{message.from_user.username} ({message.from_user.id})</b> \nДата и время: <i>{message.date.date()} {message.date.time()}</i>"
			await bot.send_photo(ADMIN_GROUP_CHAT_ID, photo=message.photo[-1].file_id, caption=msg)
			return
		if message.document:
			msg = f"От: <b>{message.from_user.username} ({message.from_user.id})</b> \nДата и время: <i>{message.date.date()} {message.date.time()}</i>"
			await bot.send_document(ADMIN_GROUP_CHAT_ID, document=message.document.file_id, caption=msg)
			return

		msg = f"<b>Поступило сообщение о проблеме!</b>\n\n{message.text}\n\nОт: <b>{message.from_user.username} ({message.from_user.id})</b> \nДата и время: <i>{message.date.date()} {message.date.time()}</i>"

	await bot.send_message(ADMIN_GROUP_CHAT_ID, msg)

async def new_anketa_to_admin_group(message, bot):
	await bot.send_message(ADMIN_GROUP_CHAT_ID, 'Поступила новая заявка в сторонники!')
	await bot.send_message(ADMIN_GROUP_CHAT_ID, message)

async def new_connect_to_admin_group(message, bot):
	msg = f"<b>Поступило обращение из раздела 'Связаться по другому вопросу'!</b>\n\n{message.text}\n\nОт: <b>{message.from_user.username} ({message.from_user.id})</b> \nДата и время: <i>{message.date.date()} {message.date.time()}</i>"

	await bot.send_message(ADMIN_GROUP_CHAT_ID, msg)


async def format_anketa (state_data):
	if state_data['eighteen'] == 'eighteen_yes':
		age_text = 'старше 18 лет'
	elif state_data['eighteen'] == 'eighteen_no':
		age_text = 'младше 18 лет'

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

	if state_data['future'] == 'future_member':
		message_text = f"<b>{state_data['member_fio']}</b>\nДень рождения: {state_data['member_birthday']}\n\nEmail: {state_data['email']}\nНомер телефона: {state_data['phone_number']}\nВозраст: {age_text}\n\nТелеграм: {state_data['tg']}\nДругие социальные сети: {state_data['social_media']}\nНомер телефона: {state_data['phone_number']}\n\nРегион постоянной регистрации {state_data['registration']}\nГород проживания: {state_data['town']}\n\nНавыки и умения: {state_data['member_skills']}\nГотов заниматься:\n{activities_text}Хочу стать {future_text}\n\nДополнительная информация: {state_data['additional_info']}"
	else:
		message_text = f"<b>{state_data['fio']}</b>\n\nEmail: {state_data['email']}\nНомер телефона: {state_data['phone_number']}\n\nВозраст: {age_text}\n\nТелеграм: {state_data['tg']}\nДругие социальные сети: {state_data['social_media']}\nНомер телефона: {state_data['phone_number']}\n\nРегион постоянной регистрации {state_data['registration']}\nГород проживания: {state_data['town']}\n\nГотов заниматься:\n{activities_text}Хочу стать {future_text}\n\nДополнительная информация: {state_data['additional_info']}"
	return message_text