"""
Вспомогательные функции для работы с данными VK API.

Содержит:
    - calculate_age: расчёт возраста из строки даты рождения;
    - get_best_size: выбор оптимального размера фотографии.
"""

from datetime import date


def calculate_age(bdate):
    """
    Вычисляет возраст по строке даты рождения.

    Поддерживает форматы:
        - "DD.MM.YYYY" — вернёт возраст;
        - "DD.MM" — вернёт None (год скрыт);
        - None или пустая строка — вернёт None.

    Args:
        bdate (str | None): Дата рождения из VK API.

    Returns:
        int | None: Возраст в годах или None, если год неизвестен.
    """
    if not bdate:
        return None

    parts = bdate.split('.')
    if len(parts) < 3:
        return None

    try:
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        birth_date = date(year, month, day)
    except (ValueError, TypeError):
        return None

    today = date.today()
    return int((today - birth_date).days // 365.2425)


def get_best_size(sizes):
    """
    Выбирает оптимальный размер фотографии для отправки.

    Приоритет типов: z → x → y → w → последний в списке.

    Args:
        sizes (list[dict]): Список размеров из VK API
                            (поле "sizes" фотографии).

    Returns:
        str | None: URL выбранного размера или None, если список пуст.
    """
    if not sizes:
        return None

    for preferred in ['z', 'x', 'y', 'w']:
        for size in sizes:
            if size.get('type') == preferred:
                return size.get('url')

    return sizes[-1].get('url')
