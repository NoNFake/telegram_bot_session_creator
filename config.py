from imports import *

@dataclass
class Config:
    # Pyrogram
    api_id: int = field(default=config('API_ID', cast=int))
    api_hash: str = field(default=config('API_HASH'))
    bot_token: str = field(default=config('BOT_TOKEN'))
    channel_id: str = field(default=config('CHANNEL_ID'))