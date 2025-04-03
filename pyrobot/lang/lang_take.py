

from pyrobot import UZ_LOAD, EN_LOAD
from dataclasses import dataclass, asdict
from typing import List, Optional
@dataclass
class User:
    user_id: int

    username: str = None
    first_name: str = None
    last_name: str = None

    lang: str = None

class Lang:
    def __init__(self, lang: str = None):
        self.lang = lang
        self.lang_data = UZ_LOAD() if lang == "uz" else EN_LOAD()

        self.user: Optional[User] = None

    def send(self, key: str):
     
        try:
            return self.lang_data[key]
        except KeyError:
            return f"[Missing: {key}]"

    def test(self):
        for key in self.lang_data:
            print(key, self.lang_data[key])
        # print(self.lang_data['start'])

        
