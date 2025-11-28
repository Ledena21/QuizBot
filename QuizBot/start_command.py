from telegram import Update
from telegram.ext import ContextTypes

class StartCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Привет! Я бот с командами в виде классов. "
            "Напиши /help, чтобы узнать больше."
        )