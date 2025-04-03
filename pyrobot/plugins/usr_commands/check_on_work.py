from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import KeyboardButton

# Errors when session isn work
from pyrogram.errors import (
    UserBlocked,
    UserBot,
    UserDeactivated,
    UserDeactivatedBan,
    UserIsBlocked,
    AuthTokenExpired,
    AuthTokenInvalid,
    AuthKeyUnregistered,
    PhoneNumberInvalid,
    PhoneNumberBanned,
    PhoneNumberUnoccupied,
    PhoneNumberOccupied,
    SessionRevoked,
    RPCError,
)

from pyrobot.pyrobot import PyroBot, UserClient
from pyrobot import *

from pyrobot.lang.lang_take import Lang, User
from pyrobot.kb.lang_kb import lang_kb
# from pyrobot.kb.count_button import main_menu_kb

@PyroBot.on_message(filters.command("check_on_work"))
async def start(_, message: Message):
    LOGGER.info(f"Start command received from user {message.from_user.id}")

    user_id = message.from_user.id
    username = message.from_user.username 
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    usr_lang = user_lang_cache.get_lang(user_id)
    lang = Lang(usr_lang)
    
    sessions = db.get_user_sessions(user_id)
    if not sessions:
        await message.reply_text(lang.send("no_sessions"))
        return  

    success = 0
    for n, (name, session_string) in enumerate(sessions):
        LOGGER.info(f"Checking session {n+1}/{len(sessions)}: {name}")
        
        try:
            user_client = UserClient(phone_number=name, session_string=session_string)
            await user_client.connect()

            me = await user_client.get_me()
            if me:
                success += 1
                LOGGER.info(f"Session {n+1} ({name}) is working properly")
        except (UserBlocked, UserBot, UserDeactivated, UserDeactivatedBan, 
                UserIsBlocked, AuthTokenExpired, AuthTokenInvalid, 
                AuthKeyUnregistered, PhoneNumberInvalid, PhoneNumberBanned, 
                PhoneNumberUnoccupied, PhoneNumberOccupied, SessionRevoked) as e:
            LOGGER.error(f"Session {n+1} ({name}) error: {e}")
            continue
        except RPCError as e:

            LOGGER.error(f"Session {n+1} ({name}) RPC error: {e}")
            continue
        except Exception as e:

            LOGGER.error(f"Session {n+1} ({name}) unexpected error: {e}")
            continue
        finally:

            if 'user_client' in locals() and user_client.is_connected:
                await user_client.disconnect()

    all_sessions = len(sessions)
    workes_sessions = success
    no_workes_sessions = all_sessions - success

    await message.reply_text(lang.send("check_on_work_text").format(all_sessions, workes_sessions, no_workes_sessions))
