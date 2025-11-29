import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
from bot import Bot

try:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("Переменная BOT_TOKEN не задана")

    bot = Bot(token=BOT_TOKEN)
    bot.start_polling()
except Exception as e:
    print(f'Error: {e}')