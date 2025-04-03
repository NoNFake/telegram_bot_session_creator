from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from pyrobot.pyrobot import PyroBot
from pyrobot import db, user_lang_cache

from pyrobot.lang.lang_take import Lang


@PyroBot.on_callback_query(filters.regex("^lang_"))
async def set_lang(_, callback_query):
    user_id = callback_query.from_user.id
    lang_code = callback_query.data.split("_")[1] # lang_uz -> uz, lang_en -> en
    
    # db.set_user_language(user_id, lang_code)
    user_lang_cache.set_lang(user_id, lang_code)
    lang = Lang(lang_code)
    
    # lang.test()
    # To show a notification/toast
    await callback_query.answer(f"Language set to {lang_code}", show_alert=False)
    
    # To edit the original message text
    await callback_query.edit_message_text(lang.send('start'))
    
