# QuizBot/tasks/vocab.py

VOCAB_HR_TO_RU = {
    "beginner": [
        {
            "question": "hvala",
            "correct": "спасибо",
            "distractors": ["добрый", "хорошо", "рад"]
        },
        {
            "question": "molim",
            "correct": "пожалуйста",
            "distractors": ["конечно", "ладно", "возьми"]
        },
        {
            "question": "bok",
            "correct": "привет",
            "distractors": ["пока", "здравствуйте", "добрый день"]
        },
        {
            "question": "kuća",
            "correct": "дом",
            "distractors": ["квартира", "здание", "комната"]
        }
    ],
    "intermediate": [
        {
            "question": "novac",
            "correct": "деньги",
            "distractors": ["работа", "время", "цена"]
        },
        {
            "question": "posao",
            "correct": "работа",
            "distractors": ["деньги", "время", "отпуск"]
        },
        {
            "question": "vrijeme",
            "correct": "время",
            "distractors": ["часы", "день", "месяц"]
        },
        {
            "question": "muškarac",
            "correct": "мужчина",
            "distractors": ["женщина", "ребёнок", "человек"]
        }
    ],
    "advanced": [
        {
            "question": "sreća",
            "correct": "счастье",
            "distractors": ["любовь", "удача", "жизнь"]
        }
    ]
}

VOCAB_RU_TO_HR = {
    "beginner": [
        {
            "question": "спасибо",
            "correct": "hvala",
            "distractors": ["zahvaljujem", "dobro", "lijepo"]
        },
        {
            "question": "пожалуйста",
            "correct": "molim",
            "distractors": ["naravno", "uzmi", "dobro"]
        },
        {
            "question": "привет",
            "correct": "bok",
            "distractors": ["zdravo", "dobar dan", "cao"]
        },
        {
            "question": "дом",
            "correct": "kuća",
            "distractors": ["stan", "soba", "zgrada"]
        }
    ],
    "intermediate": [
        {
            "question": "деньги",
            "correct": "novac",
            "distractors": ["posao", "vrijeme", "cijena"]
        },
        {
            "question": "работа",
            "correct": "posao",
            "distractors": ["novac", "vrijeme", "odmor"]
        },
        {
            "question": "время",
            "correct": "vrijeme",
            "distractors": ["sat", "dan", "mjesec"]
        },
        {
            "question": "мужчина",
            "correct": "muškarac",
            "distractors": ["žena", "dijete", "čovjek"]
        }
    ],
    "advanced": [
        {
            "question": "счастье",
            "correct": "sreća",
            "distractors": ["ljubav", "sreća", "život"]
        }
    ]
}