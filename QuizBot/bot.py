# bot.py

import asyncio
from datetime import datetime
from telegram.ext import Application
from command_processor import CommandProcessor
from commands.reminder_command import ReminderCommand


class Bot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.processor = CommandProcessor(self.application)
        self.processor.register_all()

    async def _reminder_loop(self):
        time = [
            (12,16),
            (21, 9),
            (21, 5),
            (21, 3),
            (21, 7),
            (21, 12),
        ]
        sent = set()

        while True:
            now = datetime.now()
            nowday = now.date()
            nowhour = now.hour
            nowmin = now.minute

            for hour, min in time:
                if nowhour == hour and nowmin == min:
                    key = (nowday, hour, min)
                    if key not in sent:
                        print(f"[Напоминание] Отправка в {hour:02d}:{min:02d}")
                        await self._send_reminders_to_all_users()
                        sent.add(key)
                        break

            await asyncio.sleep(60)

    async def _send_reminders_to_all_users(self):
        from progress_manager import _progress
        for user_id in _progress:
            try:
                await ReminderCommand.send_daily_reminder(self.application, user_id)
            except Exception as e:
                print(f"Не удалось отправить напоминание пользователю {user_id}: {e}")

    def start_polling(self):
        print("Бот запущен.")
        loop = asyncio.get_event_loop()
        loop.create_task(self._reminder_loop())
        self.application.run_polling()