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
        target_times = [
            (21, 47),
            (21, 30),
            (21, 50),
            (22, 20),
            (22, 00),
            (21, 29),
        ]
        last_sent = set()

        while True:
            now = datetime.now()
            current_day = now.date()
            current_hour = now.hour
            current_minute = now.minute

            for hour, minute in target_times:
                if current_hour == hour and current_minute == minute:
                    key = (current_day, hour, minute)
                    if key not in last_sent:
                        print(f"[Напоминание] Отправка в {hour:02d}:{minute:02d}")
                        await self._send_reminders_to_all_users()
                        last_sent.add(key)
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