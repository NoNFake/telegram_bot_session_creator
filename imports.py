# Pyrogram imports
from pyrogram import Client, filters, __version__ as pyro_version
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerChannel
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode



# buttons import
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from pyrogram import InlineKeyboardButton, InlineKeyboard, enums
# from pyrogram import InlineKeyboard
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultCachedAudio,
    InlineQueryResultCachedDocument,
    InlineQueryResultCachedAnimation,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedSticker,
    InlineQueryResultCachedVideo,
    InlineQueryResultCachedVoice,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InlineQueryResultContact,
    InlineQueryResultDocument,
    InlineQueryResultAnimation,
    InlineQueryResultLocation,
    InlineQueryResultPhoto,
    InlineQueryResultVenue,
    InlineQueryResultVideo,
    InlineQueryResultVoice,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from time import time, sleep



# other
from decouple           import config
from dataclasses        import asdict, dataclass, field
from typing             import List, Dict, Union, Any
import json

# my
from config import Config