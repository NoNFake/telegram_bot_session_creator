from imports import *
from pyrobot import BOT_SESSION, LOGGER, SESSIONS_PATH
from .take_proxy import get_random_proxy


from .device_gen import generate_device

config = Config()
API_ID = config.api_id
API_HASH = config.api_hash
BOT_TOKEN = config.bot_token

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("Need API_ID, API_HASH and BOT_TOKEN in .env file")

class PyroBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            
            name='pyrobot',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,


            # workers=16
            sleep_threshold=60,
            parse_mode=ParseMode.MARKDOWN,

            workdir=BOT_SESSION

        )
        self.channel_id = config.channel_id

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        # print(usr_bot_me)
        print("\n\n")
        print(" ############## START ##############")
        print(f"Pyrogram version: {pyro_version}")
        print(f"Bot started. Bot username: {usr_bot_me.username}")

    
    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")


class UserClient(Client):
    def __init__(self, phone_number: str, session_string: str = None):
        name = self.__class__.__name__.lower()

        super().__init__(
            name=phone_number,
            
            session_string=session_string,
            
            api_id=API_ID,
            api_hash=API_HASH,
            plugins=dict(root=f"{name}/plugins"),
            workdir=SESSIONS_PATH,

        
            device_model=generate_device()['device_model'],
            system_version=generate_device()['system_version'],
            app_version=generate_device()['app_version'],
            
            proxy=get_random_proxy()
        )

    async def start(self):
        await super().start()
        print(f"UserClient started. Session name: {self.session_name}")

    
    async def stop(self, *args):
        await super().stop()
        print("UserClient stopped. Bye.")


    async def restart(self):
        await self.stop()
        await self.start()

    # maybe errors
    def __aexit__(self, *args):
        return super().__aexit__(*args)

    
    
    
