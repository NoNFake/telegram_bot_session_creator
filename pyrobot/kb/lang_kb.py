from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


lang_kb = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
    ]
])