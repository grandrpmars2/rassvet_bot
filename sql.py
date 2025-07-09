import sqlite3
from config import GENERAL_ADMIN_ID, GENERAL_ADMIN_USERNAME, INITIAL_MESSAGE, INITIAL_MESSAGE_TYPE

def start_db():
	connection = sqlite3.connect('database.db')
	cursor = connection.cursor()

	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Admins (
	telegram_id TEXT,
	username TEXT PRIMARY KEY)
	''')

	cursor.execute('''
	CREATE TABLE IF NOT EXISTS Admin_messages (
	type INTEGER NOT NULL PRIMARY KEY,
	message TEXT NOT NULL)
	''')

	try:
		cursor.execute('INSERT INTO Admins (telegram_id, username) VALUES (?, ?)', (GENERAL_ADMIN_ID, GENERAL_ADMIN_USERNAME)) # добавляем первого админа
	except sqlite3.IntegrityError:
		pass

	try:
		cursor.execute('INSERT INTO Admin_messages (type, message) VALUES (?, ?)', (INITIAL_MESSAGE_TYPE, INITIAL_MESSAGE)) # добавляем базовое приветственное сообщение
	except sqlite3.IntegrityError:
		pass

	connection.commit()

	return cursor, connection