#from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import ADMIN_GROUP_CHAT_ID
import sql_functions

class AdminFilter(BaseFilter):
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection
        
    async def __call__(self, message: Message) -> bool:
        admins_usernames = sql_functions.get_admins_list(self.cursor, self.connection)
        if message.from_user.username in admins_usernames:
            return True
        else:
            return False

class ChatFilter(BaseFilter):
    def __init__(self, block_basic_functions_in_admin_chat = False):
        self.block_basic_functions_in_admin_chat = block_basic_functions_in_admin_chat
        
    async def __call__(self, message: Message) -> bool:
        if message.chat.type == 'private':
            return True
        else:
            if str(message.chat.id) == ADMIN_GROUP_CHAT_ID:
                print('block_basic_functions_in_admin_chat == ' + str(self.block_basic_functions_in_admin_chat))
                if self.block_basic_functions_in_admin_chat == True:
                    return False
                else:
                  return True
            else:
                return False

class ReplyFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        if message.reply_to_message:
            return True
        else:
            return False