# commands/help_command.py
from telegram import Update
from telegram.ext import ContextTypes

class HelpCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📚 Доступные команды:\n"
            "/start — приветствие\n"
            "/help — эта справка\n"
            "/word — учить слово\n"
            "/fact — интересный факт\n"
            "/progress — показать прогресс\n"
            "/restart — сбросить весь прогресс"
        )