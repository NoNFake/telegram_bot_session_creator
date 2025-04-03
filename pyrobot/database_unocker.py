import subprocess
import os

from pyrobot import BOT_SESSION, LOGGER, SQL_DATA

def unlock_database():
    try:
        sessions_file = [
            f for f in BOT_SESSION.iterdir() if f.is_file()
            and f.suffix == ".session" and '-jurnal' not in f.name
        ]
        LOGGER.debug(f"Sessions: {sessions_file}")
        for session in sessions_file:
            result = subprocess.run(['fuser',session], capture_output=True, text=True, check=True)
            pid = result.stdout.strip()
            if pid:
                os.system(f'kill -9 {pid}')
                LOGGER.info(f"Killed session {session.name} with pid {pid}")
    except subprocess.CalledProcessError as e:
        LOGGER.info("Database isn't locked")
    except Exception as e:
        LOGGER.error(f"Error: {e}")

def unlock_db():
    try:
        LOGGER.debug(f"DB: {SQL_DATA}")
        
        result = subprocess.run(['fuser',SQL_DATA], capture_output=True, text=True, check=True)
        pid = result.stdout.strip()
        if pid:
            os.system(f'kill -9 {pid}')
            LOGGER.info(f"Killed session {SQL_DATA.name} with pid {pid}")
    except subprocess.CalledProcessError as e:
        LOGGER.info("Database isn't locked")
    except Exception as e:
        LOGGER.error(f"Error: {e}")