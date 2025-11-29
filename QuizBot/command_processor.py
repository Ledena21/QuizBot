# command_processor.py
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
"""
Application - основной объект бота из python-telegram-bot.
CommandHandler - обработчик текстовых команд вроде /start.
CallbackQueryHandler - обработчик нажатий на кнопки
"""
from commands.start_command import StartCommand
from commands.help_command import HelpCommand
from commands.word_command import WordCommand
from commands.progress_command import ProgressCommand
from commands.restart_command import RestartCommand

class CommandProcessor:
    def __init__(this, application: Application):
        this.app = application

    def register_all(this):
        this.app.add_handler(CommandHandler("start", StartCommand.execute))
        this.app.add_handler(CommandHandler("help", HelpCommand.execute))
        this.app.add_handler(CommandHandler("word", WordCommand.execute))
        this.app.add_handler(CommandHandler("progress", ProgressCommand.execute))
        this.app.add_handler(CommandHandler("restart", RestartCommand.execute))
        this.app.add_handler(CallbackQueryHandler(WordCommand.handle_word_answer))