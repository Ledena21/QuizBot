# commands/word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
from QuizBot.tasks.vocab import VOCAB
from QuizBot.progress_manager import (
    get_user_data,
    is_level_complete,
    save_progress,
    _progress,
    LEVELS
)

class WordCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        global _progress
        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)
        level = user_data["level"]
        words = VOCAB.get(level, [])

        if not words:
            await update.message.reply_text("Нет слов на этом уровне.")
            return

        learned_ids = user_data["progress"][level]
        available = [i for i in range(len(words)) if i not in learned_ids]

        if not available:
            await update.message.reply_text(
                "Вы выучили все слова этого уровня! Напишите /word ещё раз, чтобы повторить."
            )
            return

        word_id = random.choice(available)
        word = words[word_id]

        if random.choice([True, False]):
            question = f"Переведи на хорватский:\n\n«{word['ru']}»"
            correct = word["hr"]
            distractors = word["distractors_hr"]
        else:
            question = f"Переведи на русский:\n\n«{word['hr']}»"
            correct = word["ru"]
            distractors = word["distractors_ru"]

        all_options = [correct] + distractors[:3]
        random.shuffle(all_options)

        context.user_data["current_word_correct"] = correct
        context.user_data["current_word_id"] = word_id

        keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in all_options]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(question, reply_markup=reply_markup)

    @staticmethod
    async def handle_word_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
        global _progress
        query = update.callback_query
        await query.answer()

        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)

        correct = context.user_data.get("current_word_correct")
        word_id = context.user_data.get("current_word_id")
        current_level = user_data["level"]

        user_data["stats"]["total_attempts"] += 1

        if query.data == correct:
            user_data["stats"]["total_correct"] += 1
            user_data["progress"][current_level].add(word_id)

            if is_level_complete(user_data, current_level, VOCAB):
                idx = LEVELS.index(current_level)
                if idx + 1 < len(LEVELS):
                    user_data["level"] = LEVELS[idx + 1]
                    msg = f"✅ Уровень '{current_level}' завершён!\nТеперь вы на уровне: **{user_data['level'].upper()}**!"
                else:
                    msg = "🏆 Поздравляем! Вы выучили все слова!"
            else:
                msg = "✅ Правильно! Молодец! 🎉"
        else:
            msg = f"❌ Неправильно.\nПравильный ответ: **{correct}**"

        save_progress(_progress)
        await query.edit_message_text(msg, parse_mode="Markdown")