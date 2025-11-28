# command_processor.py
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from start_command import StartCommand
from help_command import HelpCommand
from word_command import WordCommand, handle_word_answer  # ← добавим обработчик

class CommandProcessor:
    def __init__(self, application: Application):
        self.app = application

    def register_all(self):
        self.app.add_handler(CommandHandler("start", StartCommand.execute))
        self.app.add_handler(CommandHandler("help", HelpCommand.execute))
        self.app.add_handler(CommandHandler("word", WordCommand.execute))
        self.app.add_handler(CallbackQueryHandler(handle_word_answer))  # ← колбэк

# Добавьте в КОНЕЦ word_command.py:

