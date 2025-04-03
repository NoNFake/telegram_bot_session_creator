from pyrogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def main_menu_kb():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Count my sessions")],
            [KeyboardButton("Check my sessions")]
        ]
    )
