from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import KeyboardButton


from pyrobot.pyrobot import PyroBot
from pyrobot import *

from pyrobot.lang.lang_take import Lang, User
from pyrobot.kb.lang_kb import lang_kb
# from pyrobot.kb.count_button import main_menu_kb

@PyroBot.on_message(filters.command("start"))
async def start(_, message: Message):
    LOGGER.info(f"Start command received from user {message.from_user.id}")

    user_id = message.from_user.id
    username = message.from_user.username 
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name


    db.save_user(user_id, username, first_name, last_name)
    
    
    usr_lang = user_lang_cache.get_lang(user_id)
    if usr_lang:
        lang = Lang(usr_lang)
        await message.reply_text(lang.send("start"))
    else:
        await message.reply_text("Choose language", reply_markup=lang_kb)

    User(user_id, username, first_name, last_name, usr_lang)

