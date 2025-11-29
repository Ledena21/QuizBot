# start_command.py
from telegram import Update
from telegram.ext import ContextTypes

class StartCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "👋 Привет! Я бот для изучения хорватского языка 🇭🇷\n"
            "Напиши /word, чтобы начать учить слова.\n"
            "Напиши /progress, чтобы посмотреть свой прогресс.\n"
            "Напиши /restart, чтобы сбросить весь прогресс."
        )