
from pathlib import Path
import random as rnd
from pyrobot.sql_data.sql import TelegramUserDatabase
import string

from pyrobot.database_unocker import unlock_db


from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import KeyboardButton


from pyrobot.pyrobot import PyroBot
from pyrobot import *

from pyrobot.lang.lang_take import Lang, User
from pyrobot.kb.lang_kb import lang_kb
# from pyrobot.kb.count_button import main_menu_kb


def fake_string():
    import struct
    import base64
    from pyrogram.storage.storage import Storage

    _STRUCT_PREFORMAT = '>B{}sH256s'
    CURRENT_VERSION = '1'

    api_id = 123456
    api_hash = "0123456789abcdef0123456789abcdef"
    dc_id = 1
    ip = b'\x7f\x00\x00\x01'  # 127.0.0.1
    port = 80
    auth_key = b'\x00' * 256
    user_id = lambda: rnd.randint(100000000, 999999999)
    bot = False
    try:
        return (
            base64.urlsafe_b64encode(
                struct.pack(
                    Storage.SESSION_STRING_FORMAT,
                    dc_id,
                    api_id,
                    None,
                    auth_key,
                    user_id(),
                    bot
                )
            ).decode().rstrip("=")
        )
    except struct.error as e:
        raise ValueError(f"Packing error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to create session string: {str(e)}")

 



@PyroBot.on_message(filters.command("test"))
async def test(_, message: Message):
    LOGGER.info(f"test command received from user {message.from_user.id}")

    # user_id = message.from_user.id
    # username = message.from_user.username 
    # first_name = message.from_user.first_name
    # last_name = message.from_user.last_name


    # db.save_user(user_id, username, first_name, last_name)
    
    
    for i in range(10):
        user_id = lambda: rnd.randint(1, 1000)
        phone_number = lambda: f'+9989{rnd.randint(1000000, 9999999)}'
        session_string = lambda: ''.join([rnd.choice(string.ascii_lowercase) for _ in range(10)])

        username = lambda: ''.join([rnd.choice(string.ascii_lowercase) for _ in range(10)])
        first_name = lambda: ''.join([rnd.choice(string.ascii_lowercase) for _ in range(10)])
        last_name = lambda: ''.join([rnd.choice(string.ascii_lowercase) for _ in range(10)])


        

        print(i)
        # db.save_user(897794210, username(), first_name(), last_name())
        db.save_session(897794210, phone_number(), fake_string())
        
    
    await message.reply_text("Success")

    # User(user_id, username, first_name, last_name, usr_lang)







