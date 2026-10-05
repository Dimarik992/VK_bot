"""
Клавиатуры для бота VKinder.

Кнопки присылают текст — бот распознаёт его в handlers.py через COMMANDS.
"""

import json
from typing import List


def _build_keyboard(buttons: List[List[dict]]) -> str:
    """Собирает JSON-строку клавиатуры для VK API."""
    return json.dumps({
        'one_time': False,
        'buttons': buttons,
    }, ensure_ascii=False)


def _button(label: str, color: str = 'secondary') -> dict:
    """Создаёт одну текстовую кнопку."""
    return {
        'action': {
            'type': 'text',
            'label': label,
            'payload': json.dumps({'button': label}),
        },
        'color': color,
    }


def main_keyboard() -> str:
    """Главное меню: поиск и избранное."""
    return _build_keyboard([
        [
            _button('Новый поиск', 'primary'),
            _button('Избранные', 'secondary'),
        ],
    ])


def candidate_keyboard() -> str:
    """Кнопки под кандидатом: в избранное и далее."""
    return _build_keyboard([
        [
            _button('В избранное', 'positive'),
            _button('Далее', 'primary'),
        ],
        [
            _button('Избранные', 'secondary'),
        ],
    ])
