import asyncio
import logging
import sql_functions

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters.command import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import BOT_TOKEN, SAVE_MESSAGE
from sql import start_db
from filters import AdminFilter, ChatFilter, ReplyFilter
from kb import beginning_keyboard, activities_keyboard, over_eighteen_markup, living_perm_krai_markup, future_member_markup, send_anketa, back_to_beginning_keybiard, soglasie_markup
from message_generators import new_message_to_admin_group, format_anketa, new_anketa_to_admin_group, new_connect_to_admin_group

class BotStates(StatesGroup):
	entering_admin_username = State() # Состояние ввода юзернейма админа
	entering_hi_message = State() # Состояние ввода приветственного сообщения

	priemnaya = State()
	chatting = State()
	anketa_storonnika = State()
	entering_email = State()
	entering_fio = State()
	entering_tg_username = State()
	entering_phone_number = State()
	living_town = State()
	social_media = State()
	additional_info = State()
	soglasie_na_obrabotku = State()

	entering_other_activity = State()

	other_question = State()
	chatting_in_other_question = State()

router = Router()
cursor, connection = start_db()
storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)

dp.include_router(router)

# Simple User Options

# Приветственное сообщение на команду /start
@router.message(
	Command('start'),
	ChatFilter(block_basic_functions_in_admin_chat=True)
)
async def hi_message(message: types.Message, state: FSMContext):
	await state.set_state(None)
	hi_message = sql_functions.get_message(cursor, connection, 1)
	keyboard = beginning_keyboard()

	try:
		await message.answer(hi_message, reply_markup = keyboard)
	except:
		await message.answer(SAVE_MESSAGE)

# Общественная приемная
@router.message(
	F.text == 'Общественная приемная',
	StateFilter(None),
	ChatFilter(block_basic_functions_in_admin_chat=True)
)
async def social_priemnaya(message: types.Message, state: FSMContext):
	await message.answer('Что у вас случилось? Опишите ситуацию.')
	await state.set_state(BotStates.priemnaya)

@router.message(BotStates.priemnaya)
async def social_priemnaya_second(message: types.Message, state: FSMContext):
	await new_message_to_admin_group(message, bot)
	await message.answer('Ваше обращение принято! Мы постараемся Вам помочь. \n Сейчас вы находитесь в режиме чата с администратором. Он свяжется с Вами и задаст уточняющие вопросы. Все отправленные сообщения будут доставлены администратору. Чтобы вернуться в меню, введите /start')
	await state.set_state(BotStates.chatting)

@router.message(BotStates.chatting)
async def chatting_in_priemnaya(message: types.Message, state: FSMContext):
	await new_message_to_admin_group(message, bot)

# Стать сторонником
@router.message(
	F.text == 'Стать сторонником',
	StateFilter(None),
	ChatFilter(block_basic_functions_in_admin_chat=True)
)
async def social_priemnaya(message: types.Message, state: FSMContext):
	await message.answer_photo(photo=types.FSInputFile('rassvet.png'), caption='<b>Присоединяйтесь к сторонникам Политической партии "Рассвет" в Пермском крае!</b>\n\nМы ищем неравнодушных граждан, желающих сделать свой город и край лучше!\nЕсли у вас есть идеи, мысли или проекты, которые вы хотели бы обсудить и реализовать вместе с нами, или же вы давно хотели стать частью нашей команды, присоединяйтесь!\n\nВнимательно заполните форму. После её проверки мы сразу же ответим вам!')
	await message.answer('Введите ваш email: ')
	await state.set_state(BotStates.entering_email)

@router.message(BotStates.entering_email)
async def social_priemnaya(message: types.Message, state: FSMContext):
	await state.update_data(email=message.text)
	await state.update_data(activity1=0, activity2=0, activity3=0, activity4=0, activity5=0, activity6=0, activity7=0, activity8=0)

	state_data = await state.get_data()
	kb = activities_keyboard(state_data)
	await message.answer('Чем вы хотели бы заниматься, будучи сторонником? В каких проектах хотели бы участвовать?', reply_markup=kb)

@router.callback_query(lambda c: c.data.startswith(('activity')))
async def activity1(callback_query: types.CallbackQuery, state: FSMContext):
	activity_number = int(callback_query.data[-1])
	state_data = await state.get_data()
	
	current_activity_status = state_data[f'activity{activity_number}']

	if current_activity_status == 0:
		new_activity_status = 1
	elif current_activity_status == 1:
		new_activity_status = 0

	if activity_number == 1:
		await state.update_data(activity1=new_activity_status)
	elif activity_number == 2:
		await state.update_data(activity2=new_activity_status)
	elif activity_number == 3:
		await state.update_data(activity3=new_activity_status)
	elif activity_number == 4:
		await state.update_data(activity4=new_activity_status)
	elif activity_number == 5:
		await state.update_data(activity5=new_activity_status)
	elif activity_number == 6:
		await state.update_data(activity6=new_activity_status)
	elif activity_number == 7:
		await state.update_data(activity7=new_activity_status)
	elif activity_number == 8:
		await state.update_data(activity8=new_activity_status)

	state_data = await state.get_data()
	new_markup = activities_keyboard(state_data)

	await callback_query.message.edit_reply_markup(reply_markup = new_markup)

@router.callback_query(lambda c: c.data.startswith(('next')))
async def activity1(callback_query: types.CallbackQuery, state: FSMContext):
	state_data = await state.get_data()
	if state_data['activity8'] == 1:
		await bot.send_message(callback_query.message.chat.id, text='Напишите то, чем хотите заниматься')
		await state.set_state(BotStates.entering_other_activity)
	else:
		await bot.send_message(callback_query.message.chat.id, text='Укажите Ваше ФИО')
		await state.set_state(BotStates.entering_fio)

@router.message(BotStates.entering_other_activity)
async def entering_fio(message: types.Message, state: FSMContext):
	await state.update_data(activity8 = message.text)

	await bot.send_message(message.chat.id, text='Укажите Ваше ФИО')
	await state.set_state(BotStates.entering_fio)

@router.message(BotStates.entering_fio)
async def entering_tg(message: types.Message, state: FSMContext):
	await state.update_data(fio = message.text)

	await bot.send_message(message.chat.id, text='Укажите Ваш ник в Telegram')
	await state.set_state(BotStates.entering_tg_username)

@router.message(BotStates.entering_tg_username)
async def entering_phone(message: types.Message, state: FSMContext):
	await state.update_data(tg = message.text)

	await bot.send_message(message.chat.id, text='Укажите Ваш номер телефона')
	await state.set_state(BotStates.entering_phone_number)

@router.message(BotStates.entering_phone_number)
async def entering_eighteen(message: types.Message, state: FSMContext):
	await state.update_data(phone_number = message.text)

	markup = over_eighteen_markup()
	await bot.send_message(message.chat.id, text='Вам уже исполнилось 18?', reply_markup=markup)

@router.callback_query(lambda c: c.data.startswith(('eighteen_')))
async def eighteen_answer(callback_query: types.CallbackQuery, state: FSMContext):
	answer = callback_query.data
	await state.update_data(eighteen=answer)

	markup = living_perm_krai_markup()
	await bot.send_message(callback_query.message.chat.id, 'Проживаете ли Вы постоянно в Пермском крае?', reply_markup=markup)

@router.callback_query(lambda c: c.data.startswith(('living_')))
async def living_perm_krai_answer(callback_query: types.CallbackQuery, state: FSMContext):
	answer = callback_query.data
	await state.update_data(living_perm_krai=answer)

	await bot.send_message(callback_query.message.chat.id, 'В каком городе вы проживаете?')
	await state.set_state(BotStates.living_town)

@router.message(BotStates.living_town)
async def living_town_answer(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(town=answer)

	markup = future_member_markup()
	await bot.send_message(message.chat.id, 'Хотели бы вы стать членом будущей партии? Необходимо будет подписать соответствующее заявление.', reply_markup=markup)

@router.callback_query(lambda c: c.data.startswith(('future_')))
async def future_member_answer(callback_query: types.CallbackQuery, state: FSMContext):
	answer = callback_query.data
	await state.update_data(future=answer)

	await bot.send_message(callback_query.message.chat.id, 'Укажите ссылки на другие ваши соц.сети')
	await state.set_state(BotStates.social_media)

@router.message(BotStates.social_media)
async def living_town_answer(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(social_media=answer)

	await bot.send_message(message.chat.id, 'Дополнительная информация, которой Вы хотели бы поделиться')
	await state.set_state(BotStates.soglasie_na_obrabotku)

@router.message(BotStates.soglasie_na_obrabotku)
async def additional_info_answer(message: types.Message, state: FSMContext):
	answer = message.text
	await state.update_data(additional_info=answer)

	markup = soglasie_markup()
	#media = types.MediaGroup()
	#file1 = types.input_media_document.InputMediaDocument()
	#file2 = types.input_media_document.InputMediaDocument(open('Сведения о реализуемых требованиях к защите персональных данных.pdf', 'rb'))
	file = types.input_file.FSInputFile('Акт оценки вреда субъектам персональных данных.pdf')
	file2 = types.input_file.FSInputFile('Сведения о реализуемых требованиях к защите персональных данных.pdf')

	await bot.send_message(message.chat.id, '<b>Согласие на обработку персональных данных</b>\n\nМы находимся на территории Российской Федерации и соблюдаем ее законы, в частности законодательство о персональных данных, поэтому нам необходимо получить Ваше согласие на их обработку. Все данные хранятся в зашифрованном виде. Некоторые документы для изучения прикреплены к этому сообщению.\n\nВы имеете право отозвать согласие на обработку персональных данных. Для этого свяжитесь с нами и отправьте письменное заявление. \n\n<b>Текст согласия:</b>\nастоящим в соответствии с Федеральным законом № 152-ФЗ «О персональных данных» от 27.07.2006 даю Оглоблину Алексею Александровичу согласие на автоматизированную и неавтоматизированную обработку персональных данных, указанных мной в анкете: сбор, систематизацию, накопление, хранение, уточнение (обновление, изменение), использование, уничтожение.\n\nНастоящее согласие распространяется на следующие персональные данные: фамилия, имя и отчество, контактный телефон, адрес электронной почты, город проживания, сведения о страницах в социальных сетях, а также другие персональные данные, сообщенные мной дополнительно.', reply_markup = markup)
	await bot.send_document(message.chat.id, file)
	await bot.send_document(message.chat.id, file2)
	await state.set_state(BotStates.additional_info)


@router.callback_query(lambda c: c.data.startswith(('soglasie_')))
async def soglasie_answer(callback_query: types.CallbackQuery, state: FSMContext):
	answer = callback_query.data.split('_')[1]

	if answer == 'no':
		await state.set_state(None)
		hi_message = sql_functions.get_message(cursor, connection, 1)
		keyboard = beginning_keyboard()

		try:
			await bot.send_message(callback_query.message.chat.id, hi_message, reply_markup = keyboard)
		except:
			await bot.send_message(callback_query.message.chat.id, SAVE_MESSAGE)

	else:
		state_data = await state.get_data()
		anketa_text = str(await format_anketa(state_data))
		markup = send_anketa()

		await bot.send_message(callback_query.message.chat.id, 'Вот как выглядит ваша анкета:')
		await bot.send_message(callback_query.message.chat.id, anketa_text, reply_markup = markup)

@router.callback_query(lambda c: c.data.startswith(('anketa_')))
async def sending_anketa(callback_query: types.CallbackQuery, state: FSMContext):
	answer = callback_query.data.split('_')[1]

	state_data = await state.get_data()
	anketa_text = await format_anketa(state_data)

	if answer == 'start':
		await state.set_state(None)
		hi_message = sql_functions.get_message(cursor, connection, 1)
		keyboard = beginning_keyboard()

		try:
			await bot.send_message(callback_query.message.chat.id, hi_message, reply_markup = keyboard)
		except:
			await bot.send_message(callback_query.message.chat.id, SAVE_MESSAGE)

	elif answer == 'send':
		await new_anketa_to_admin_group(anketa_text, bot)
		#markup = back_to_beginning_keybiard()
		await bot.send_message(callback_query.message.chat.id, 'Анкета отправлена, поздравляем! Наши модераторы Вам ответят сразу после того, как ее обработают. Чтобы вернуться в начало, введите /start или нажмите на кнопку')
		await state.set_state(None)

@router.message(
	F.text == 'Вернуться в начало',
	ChatFilter(block_basic_functions_in_admin_chat=True)
)
async def back_to_beginning(message: types.Message, state: FSMContext):
	await state.set_state(None)
	hi_message = sql_functions.get_message(cursor, connection, 1)
	keyboard = beginning_keyboard()

	try:
		await bot.send_message(message.chat.id, hi_message, reply_markup = keyboard)
	except:
		await bot.send_message(message.chat.id, SAVE_MESSAGE)

# Связаться по другому вопросу
@router.message(
	F.text == 'Связаться по другому вопросу',
	StateFilter(None),
	ChatFilter(block_basic_functions_in_admin_chat=True)
)
async def connect(message: types.Message, state: FSMContext):
	await message.answer('Что вы хотите сообщить?')
	await state.set_state(BotStates.other_question)

@router.message(BotStates.other_question)
async def connect_second(message: types.Message, state: FSMContext):
	await new_connect_to_admin_group(message, bot)
	await message.answer('Ваше обращение принято! Мы постараемся Вам помочь. \n Сейчас вы находитесь в режиме чата с администратором. Он свяжется с Вами и задаст уточняющие вопросы. Все отправленные сообщения будут доставлены администратору. Чтобы вернуться в меню, введите /start')
	await state.set_state(BotStates.chatting_in_other_question)

@router.message(BotStates.chatting_in_other_question)
async def chatting_in_connect(message: types.Message, state: FSMContext):
	await new_connect_to_admin_group(message, bot)
	await message.answer('Ваше сообщение отправлено.')

# editing hi message
@router.message(Command('update_message'), StateFilter(None), ChatFilter())
async def update_message(message: types.Message, state: FSMContext):
	await message.reply("Отправьте новое приветственное сообщение!")
	await state.set_state(BotStates.entering_hi_message)

@router.message(BotStates.entering_hi_message)
async def update_message2(message: types.Message, state: FSMContext):
	try:
		sql_functions.edit_message(cursor, connection, 1, message.text)
		await message.reply("Новое приветственное сообщение установлено!")
	except:
		await message.reply("Что-то пошло не так. Попробуйте снова")
	await state.set_state(None)

# Answering in Group Admin Chat
#фильтр, что это реплай на сообщение
@router.message(ChatFilter(), ReplyFilter())
async def answer_message(message: types.Message):
	text = message.reply_to_message.text
	to_user_id = text.split('(')[1].split(')')[0]
	to_user_username = text.split(':')[1].split('(')[0].strip()
	try:
		await bot.send_message(int(to_user_id), message.text)
	except:
		await message.answer(f'Что-то пошло не так. Попробуйте написать пользователю напрямую – @{to_user_username}')


async def main():
	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(main())
	connection.close()