from .pyrobot import PyroBot
from .database_unocker import unlock_database, unlock_db
from .pyrobot import LOGGER
from imports import *


# import asyncio

# async def main():
#     print("Checking database...")
#     unlock_database()

#     sleep(1)
#     PyroBot().run()
#     # try:
#     #     PyroBot().run()
#     # except KeyboardInterrupt:
#     #     PyroBot().stop()
#     #     LOGGER.info("Bot stopped. Exiting...")
#     #     exit(0)

if __name__ == '__main__':
    print("Checking database...")
    unlock_database()

    print("Checking DB...")
    unlock_db()


    sleep(1)
    PyroBot().run()



    
    # try:
    #     PyroBot().run()
    # except KeyboardInterrupt:
    #     PyroBot().stop()
    #     LOGGER.info("Bot stopped. Exiting...")
    #     exit(0)