# progress_manager.py
import json
import os
from typing import Dict, Set

PROGRESS_FILE = "user_progress.json"
LEVELS = ["beginner", "intermediate", "advanced"]

def load_progress() -> Dict[str, dict]:
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for user_id, user_data in data.items():
                    if "progress" in user_data:
                        user_data["progress"] = {
                            level: set(ids) for level, ids in user_data["progress"].items()
                        }
                    if "progress" not in user_data:
                        user_data["progress"] = {}
                    for level in LEVELS:
                        if level not in user_data["progress"]:
                            user_data["progress"][level] = set()
                return data
        except Exception as e:
            print(f"ERROR: {e}")
            return {}
    return {}

def save_progress(data: Dict[str, dict]):
    serializable = {}
    for user_id, user_data in data.items():
        if "progress" not in user_data:
            user_data["progress"] = {}
        for level in LEVELS:
            if level not in user_data["progress"]:
                user_data["progress"][level] = set()

        serializable[user_id] = {
            "level": user_data["level"],
            "stats": user_data["stats"],
            "progress": {
                level: list(ids) for level, ids in user_data["progress"].items()
            }
        }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

def get_user_data(progress_dict: dict, user_id: str) -> dict:
    if user_id not in progress_dict:
        progress_dict[user_id] = {
            "level": "beginner",
            "stats": {"total_correct": 0, "total_attempts": 0},
            "progress": {}
        }

    user_data = progress_dict[user_id]

    for level in LEVELS:
        if level not in user_data["progress"]:
            user_data["progress"][level] = set()
    if "reminder_skip_count" not in user_data:
        user_data["reminder_skip_count"] = 0
    if "streak_days" not in user_data:
        user_data["streak_days"] = 0

    return user_data

def is_level_complete(user_data: dict, level: str, vocab: dict) -> bool:
    words = vocab.get(level, [])
    learned = user_data["progress"].get(level, set())
    return len(learned) >= len(words) and len(words) > 0

_progress = load_progress()