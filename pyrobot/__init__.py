import logging
from pathlib import Path
import json
from pyrobot.sql_data.sql import TelegramUserDatabase
from dataclasses import dataclass, asdict



logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.DEBUG)

# Logger
LOGGER = logging.getLogger(__name__)
LOGGER.info("Logger inited")

# Sessions
BASE_DIR = Path(__file__).parent
BOT_SESSION =  BASE_DIR / "bot_session"

DATA = BASE_DIR / "data"

SESSIONS_PATH = DATA / "sessions"
SESSIONS_PATH.mkdir(exist_ok=True)

SESSIONS = lambda: [file for file in SESSIONS_PATH.iterdir() if file.is_file() and file.suffix == ".session" and "-journal" not in file.name]

LOGGER.info(f"SESSIONS: {SESSIONS()}")
LOGGER.info(f"BASE_DIR: {BASE_DIR}")
LOGGER.info(f"BOT_SESSION: {BOT_SESSION}")


# Database SQL
SQL_DATA = DATA / "users_db"
SQL_DATA.mkdir(exist_ok=True)

# Database
DATABASE = SQL_DATA / "users.db"
DATABASE.touch(exist_ok=True)

db = TelegramUserDatabase(DATABASE)

# LANGUAGES
LANG = BASE_DIR / "lang"
UZ_LANG = LANG / "uz.json"
EN_LANG = LANG / "en.json"
ALL_LANG = LANG / "lang.json"

UZ_LOAD = lambda: json.load(open(UZ_LANG))
EN_LOAD = lambda: json.load(open(EN_LANG))
LANG_LOAD = lambda: json.load(open(ALL_LANG))



    # def to_dict(self):
    #     return asdict(self)
    
    # @classmethod
    # def from_dict(cls, data: dict):
    #     return cls(**data)


# Proxy
PROXY_PATH = DATA / "proxy"
PROXY_PATH.mkdir(exist_ok=True)

PROXY = PROXY_PATH / "proxy.txt"
PROXY.touch(exist_ok=True)

Path(BOT_SESSION).mkdir(exist_ok=True)



# lang
class UserLanguageCache:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserLanguageCache, cls).__new__(cls)
            cls._instance._cache = {}
        return cls._instance
    
    def get_lang(self, user_id: int):
        """Get language from cache or database"""
        if user_id not in self._cache:
            lang = db.get_user_language(user_id)
            if lang:
                self._cache[user_id] = lang
            return lang
        return self._cache[user_id]
    
    def set_lang(self, user_id: int, lang: str):
        """Update language in both cache and database"""
        self._cache[user_id] = lang
        db.set_user_language(user_id, lang)

# Create instance of cache
user_lang_cache = UserLanguageCache()
