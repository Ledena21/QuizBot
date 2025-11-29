# commands/word_command.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import random
from QuizBot.tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from QuizBot.progress_manager import _progress, get_user_data

class WordCommand:
    @staticmethod
    async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)
        level = user_data["level"]

        # Случайный выбор направления перевода
        if random.choice([True, False]):
            vocab = VOCAB_RU_TO_HR
            direction = "ru_to_hr"
            prefix = "Переведи на хорватский:\n\n«"
            suffix = "»"
        else:
            vocab = VOCAB_HR_TO_RU
            direction = "hr_to_ru"
            prefix = "Переведи на русский:\n\n«"
            suffix = "»"

        words = vocab.get(level, [])
        if not words:
            await update.message.reply_text("Нет слов на этом уровне.")
            return

        learned = user_data["progress"][level]
        available = [i for i in range(len(words)) if i not in learned]

        if not available:
            await update.message.reply_text("Вы выучили все слова этого уровня!")
            return

        word_id = random.choice(available)
        word = words[word_id]

        # Формируем вопрос
        question = f"{prefix}{word['question']}{suffix}"
        correct = word["correct"]
        distractors = word["distractors"][:3]

        all_options = [correct] + distractors
        random.shuffle(all_options)

        # Сохраняем данные для проверки
        context.user_data["current_word_id"] = word_id
        context.user_data["current_word_correct"] = correct
        context.user_data["current_vocab_direction"] = direction
        context.user_data["current_vocab_level"] = level

        keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in all_options]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(question, reply_markup=reply_markup)

    @staticmethod
    async def handle_word_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from QuizBot.progress_manager import save_progress, LEVELS

        global _progress
        query = update.callback_query
        await query.answer()

        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)

        correct = context.user_data.get("current_word_correct")
        word_id = context.user_data.get("current_word_id")
        level = context.user_data.get("current_vocab_level")

        user_data["stats"]["total_attempts"] += 1

        if query.data == correct:
            user_data["stats"]["total_correct"] += 1
            user_data["progress"][level].add(word_id)

            # Используем VOCAB_RU_TO_HR для подсчёта общего числа слов на уровне
            from QuizBot.tasks.vocab import VOCAB_RU_TO_HR
            total_words = len(VOCAB_RU_TO_HR[level])
            if len(user_data["progress"][level]) == total_words:
                idx = LEVELS.index(level)
                if idx + 1 < len(LEVELS):
                    user_data["level"] = LEVELS[idx + 1]
                    msg = f"✅ Уровень '{level}' завершён!\nТеперь вы на уровне: **{user_data['level'].upper()}**!"
                else:
                    msg = "🏆 Поздравляем! Вы выучили все слова!"
            else:
                msg = "✅ Правильно! Молодец! 🎉"
        else:
            msg = f"❌ Неправильно.\nПравильный ответ: **{correct}**"

        save_progress(_progress)
        await query.edit_message_text(msg, parse_mode="Markdown")