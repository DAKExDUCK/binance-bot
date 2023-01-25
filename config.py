import os

from aiogram import Bot, types
from dotenv import load_dotenv

load_dotenv()

admin_id = os.getenv('admin_id')
TOKEN = os.getenv('TOKEN')
# TOKEN="5858736437:AAFtcv8mAM7B_5YmHabBmCwGXidz4DnxfP0"
# admin_id=789979787

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)


chrome_options = [
    '--headless',
    'window-size=1920,1080',
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    '--disable-gpu', "--no-sandbox",
    "--disable-dev-shm-usage", "--disable-crash-reporter",
    "--log-level=3", "--disable-extensions",
    "--disable-in-process-stack-traces", "--disable-logging",
    "--output=/dev/null",
    "--disable-features=Translate",
    "--force-device-scale-factor=1"
    ]