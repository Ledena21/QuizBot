# === Настройка event loop на Windows ===
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# === Остальное ===
import os
from bot import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ Переменная BOT_TOKEN не задана!")

def main():
    bot = Bot(token=BOT_TOKEN)
    bot.start_polling()  # ← синхронный вызов

if __name__ == "__main__":
    main()