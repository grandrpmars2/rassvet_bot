import sqlite3

from config import GENERAL_ADMIN_USERNAME

def get_admins_list(cursor, connection):
	admins_list = []
	cursor.execute('SELECT username FROM Admins')
	got_list = cursor.fetchall()
	for admin in got_list:
		admins_list.append(admin[0])
	return admins_list

def add_admin(cursor, connection, telegram_id, username):
	cursor.execute('INSERT INTO Admins (telegram_id, username) VALUES (?, ?)', (telegram_id, username))
	connection.commit()

def delete_admin(cursor, connection, username):
	if username == GENERAL_ADMIN_USERNAME:
		return False
		
	try:
		cursor.execute('DELETE FROM Admins WHERE username = ?', (username, ))
		connection.commit()
		return True
	except:
		return False


def get_message (cursor, connection, msg_type):
	cursor.execute('SELECT message from Admin_messages WHERE type = ?', (msg_type,))
	message = cursor.fetchone()[0]
	return message

def edit_message(cursor, connection, msg_type, new_message):
	cursor.execute('UPDATE Admin_messages SET message = ? WHERE type = ?', (new_message, msg_type))
	connection.commit()