# vocab.py
VOCAB = {
    "beginner": [
        {
            "ru": "спасибо",
            "hr": "hvala",
            "distractors_ru": ["добрый", "хорошо", "рад"],
            "distractors_hr": ["zahvaljujem", "dobro", "lijepo"]
        },
        {
            "ru": "пожалуйста",
            "hr": "molim",
            "distractors_ru": ["конечно", "ладно", "возьми"],
            "distractors_hr": ["naravno", "uzmi", "dobro"]
        },
        {
            "ru": "привет",
            "hr": "bok",
            "distractors_ru": ["пока", "здравствуйте", "добрый день"],
            "distractors_hr": ["zdravo", "dobar dan", "cao"]
        },
        {
            "ru": "дом",
            "hr": "kuća",
            "distractors_ru": ["квартира", "здание", "комната"],
            "distractors_hr": ["stan", "soba", "zgrada"]
        }
    ],
    "intermediate": [  # ← ДОБАВЬТЕ СЛОВА!
        {
            "ru": "деньги",
            "hr": "novac",
            "distractors_ru": ["работа", "время", "цена"],
            "distractors_hr": ["posao", "vrijeme", "cijena"]
        },
        {
            "ru": "работа",
            "hr": "posao",
            "distractors_ru": ["деньги", "время", "отпуск"],
            "distractors_hr": ["novac", "vrijeme", "odmor"]
        },
        {
            "ru": "время",
            "hr": "vrijeme",
            "distractors_ru": ["часы", "день", "месяц"],
            "distractors_hr": ["sat", "dan", "mjesec"]
        },
        {
            "ru": "мужчина",
            "hr": "muškarac",
            "distractors_ru": ["женщина", "ребёнок", "человек"],
            "distractors_hr": ["žena", "dijete", "čovjek"]
        }
    ],
    "advanced": [  # ← можно добавить позже
        {
            "ru": "счастье",
            "hr": "sreća",
            "distractors_ru": ["любовь", "удача", "жизнь"],
            "distractors_hr": ["ljubav", "sreća", "život"]
        }
    ]
}