from telegram import Update
from telegram.ext import ContextTypes

class HelpCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Доступные команды:\n"
            "/start — начать\n"
            "/help — показать эту справку"
        )