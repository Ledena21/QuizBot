from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import telegram
from progress_manager import _progress, get_user_data, save_progress, LEVELS
from tasks.vocab import VOCAB_RU_TO_HR, VOCAB_HR_TO_RU
from tasks.facts import FACTS
from commands.reminder_command import ReminderCommand


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is None:
        return
    query = update.callback_query
    try:
        await query.answer()
    except telegram.error.BadRequest as e:
        if "Query is too old" in str(e):
            return
        else:
            raise

    user_id = str(update.effective_user.id)
    user_data = get_user_data(_progress, user_id)
    data = query.data

    if data.startswith("fact_advice|"):
        parts = data.split("|", 3)
        if len(parts) != 3:
            await query.edit_message_text("Ошибка данных (подсказка).")
            return
        _, level, item_id_str = parts
        try:
            item_id = int(item_id_str)
        except ValueError:
            await query.edit_message_text("Некорректный ID факта.")
            return
        if level not in FACTS or item_id >= len(FACTS[level]):
            await query.edit_message_text("Факт не найден.")
            return
        advice = FACTS[level][item_id].get("advice", "Подсказка недоступна.")
        await query.message.reply_text(f"{advice}", parse_mode="Markdown")
        return

    if data.startswith("word|"):
        parts = data.split("|", 5)
        if len(parts) != 5:
            await query.edit_message_text("Ошибка данных (слово).")
            return
        _, direction, level, item_id_str, opt_index_str = parts
        item_id = int(item_id_str)
        opt_index = int(opt_index_str)
        vocab = VOCAB_RU_TO_HR if direction == "ru_to_hr" else VOCAB_HR_TO_RU
        if level not in vocab or item_id >= len(vocab[level]):
            await query.edit_message_text("Слово не найдено.")
            return
        item = vocab[level][item_id]
        options = [item["correct"]] + item["distractors"][:3]
        if opt_index < 0 or opt_index >= len(options):
            await query.edit_message_text("Ошибка: вариант ответа не существует.")
            return
        userchoice = options[opt_index]
        correct = item["correct"]
        is_word = True

    elif data.startswith("fact|"):
        parts = data.split("|", 4)
        if len(parts) != 4:
            await query.edit_message_text("Ошибка данных (факт).")
            return
        _, level, item_id_str, opt_index_str = parts
        item_id = int(item_id_str)
        opt_index = int(opt_index_str)
        if level not in FACTS or item_id >= len(FACTS[level]):
            await query.edit_message_text("Факт не найден.")
            return
        item = FACTS[level][item_id]
        options = [item["correct"]] + item["distractors"][:3]
        if opt_index < 0 or opt_index >= len(options):
            await query.edit_message_text("Ошибка: вариант ответа не существует.")
            return
        userchoice = options[opt_index]
        correct = item["correct"]
        is_word = False
        vocab = None

    else:
        await query.edit_message_text("Неизвестный тип запроса.")
        return

    original_keyboard = query.message.reply_markup.inline_keyboard
    original_texts = []
    for row in original_keyboard:
        btn = row[0]
        text = btn.text
        if text.startswith(("✅ ", "❌ ")):
            text = text[2:]
        if text == "Подсказка":
            continue
        original_texts.append(text)

    new_keyboard = []
    for i, text in enumerate(original_texts):
        if text == userchoice:
            btn_text = "✅ " + text if userchoice == correct else "❌ " + text
        elif text == correct and userchoice != correct:
            btn_text = "✅ " + text
        else:
            btn_text = text
        if is_word:
            callback_data = f"word|{direction}|{level}|{item_id}|{i}"
        else:
            callback_data = f"fact|{level}|{item_id}|{i}"
        new_keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])

    if not is_word:
        new_keyboard.append([InlineKeyboardButton("Подсказка", callback_data=f"fact_advice|{level}|{item_id}")])

    try:
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(new_keyboard))
    except Exception as e:
        print(f"Ошибка обновления клавиатуры: {e}")

    user_data["stats"]["total_attempts"] += 1  # ← ВСЕГДА увеличиваем попытки
    is_correct = (userchoice == correct)
    if is_correct:
        user_data["stats"]["total_correct"] += 1
        if is_word:
            user_data["progress"][level].add(item_id)
            total_words = len(vocab[level])
            if len(user_data["progress"][level]) == total_words:
                idx = LEVELS.index(level)
                if idx + 1 < len(LEVELS):
                    user_data["level"] = LEVELS[idx + 1]
        msg = "Правильно!"
    else:
        msg = f"Неправильно.\nПравильный ответ: **{correct}**"

    save_progress(_progress)

    session = user_data.get("test_session")
    if session is not None:
        if is_correct:
            session["correct_count"] += 1
        session["current"] += 1
        save_progress(_progress)
        await ReminderCommand._send_next_test_question(
            context.bot,
            update.effective_chat.id,
            user_id
        )
    else:
        await query.message.reply_text(msg, parse_mode="Markdown")