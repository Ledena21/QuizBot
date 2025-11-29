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

        question = f"{prefix}{word['question']}{suffix}"
        correct = word["correct"]
        distractors = word["distractors"][:3]

        all_options = [correct] + distractors
        random.shuffle(all_options)

        # ← ВАЖНО: callback_data с префиксом word|
        keyboard = []
        for opt in all_options:
            cb = f"word|{direction}|{level}|{word_id}|{opt}"
            keyboard.append([InlineKeyboardButton(opt, callback_data=cb)])

        await update.message.reply_text(question, reply_markup=InlineKeyboardMarkup(keyboard))

    @staticmethod
    async def handle_word_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from QuizBot.progress_manager import save_progress, LEVELS

        global _progress
        query = update.callback_query
        await query.answer()

        data = query.data
        parts = data.split("|", 5)
        if len(parts) != 5:
            await query.edit_message_text("⚠️ Некорректные данные.")
            return

        _, direction, level, word_id_str, user_choice = parts
        word_id = int(word_id_str)

        # Получаем правильный ответ из нужного словаря
        if direction == "ru_to_hr":
            from QuizBot.tasks.vocab import VOCAB_RU_TO_HR
            vocab = VOCAB_RU_TO_HR
        else:
            from QuizBot.tasks.vocab import VOCAB_HR_TO_RU
            vocab = VOCAB_HR_TO_RU

        if level not in vocab or word_id >= len(vocab[level]):
            await query.edit_message_text("⚠️ Слово не найдено.")
            return

        correct = vocab[level][word_id]["correct"]

        # Обновляем прогресс и статистику
        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(_progress, user_id)

        user_data["stats"]["total_attempts"] += 1

        if user_choice == correct:
            user_data["stats"]["total_correct"] += 1
            user_data["progress"][level].add(word_id)

            # Проверка завершения уровня
            total_words = len(vocab[level])
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