# command_processor.py
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import Update
from telegram.ext import ContextTypes
from commands.start_command import StartCommand
from commands.help_command import HelpCommand
from commands.word_command import WordCommand
from commands.fact_command import FactCommand
from commands.progress_command import ProgressCommand
from commands.restart_command import RestartCommand

class CommandProcessor:
    def __init__(self, application: Application):
        self.app = application

    def register_all(self):
        self.app.add_handler(CommandHandler("start", StartCommand.execute))
        self.app.add_handler(CommandHandler("help", HelpCommand.execute))
        self.app.add_handler(CommandHandler("word", WordCommand.execute))
        self.app.add_handler(CommandHandler("fact", FactCommand.execute))
        self.app.add_handler(CommandHandler("progress", ProgressCommand.execute))
        self.app.add_handler(CommandHandler("restart", RestartCommand.execute))
        # Один общий хендлер для всех кнопок
        self.app.add_handler(CallbackQueryHandler(self._handle_callback))

    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data

        # Если это факт — обрабатываем через FactCommand
        if data.startswith("fact|"):
            await FactCommand.handle_fact_answer(update, context)
        # Если это слово — обрабатываем через WordCommand
        elif data.startswith("word|"):
            await WordCommand.handle_word_answer(update, context)
        else:
            await query.answer()
            await query.edit_message_text("⚠️ Неизвестный тип запроса.")