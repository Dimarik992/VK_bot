"""
Модуль для работы с пользователями VK API.

Содержит функции:
    - get_user_info: получение данных о пользователе;
    - search_candidates: поиск кандидатов для знакомств;
    - get_candidate_with_photos: обёртка «кандидат + топ-3 фото».
"""

from vk_service.auth import vk
from vk_service.photos import get_top_photos
from vk_service.utils import calculate_age


def get_user_info(user_id):
    """
    Возвращает информацию о пользователе VK.

    Запрашивает поля: пол, дата рождения, город.

    Args:
        user_id (int | str): ID пользователя VK.

    Returns:
        dict | None: Словарь с полями:
            - id (int): ID пользователя;
            - first_name (str): Имя;
            - last_name (str): Фамилия;
            - sex (int | None): 1 — женский, 2 — мужской;
            - age (int | None): Возраст или None;
            - city_id (int | None): ID города;
            - city_title (str | None): Название города.
        Возвращает None, если пользователь не найден.
    """
    result = vk.users.get(
        user_ids=user_id,
        fields='sex, bdate, city',
    )

    if not result:
        return None

    user = result[0]
    city = user.get('city') or {}

    return {
        'id': user.get('id'),
        'first_name': user.get('first_name'),
        'last_name': user.get('last_name'),
        'sex': user.get('sex'),
        'age': calculate_age(user.get('bdate')),
        'city_id': city.get('id'),
        'city_title': city.get('title'),
    }


def search_candidates(user_info, count=50, offset=0):
    """
    Ищет кандидатов для знакомств по данным пользователя.

    Критерии поиска:
        - пол — противоположный полу клиента;
        - возраст — ±3 года от возраста клиента;
        - город — тот же, что у клиента;
        - только пользователи с фото;
        - только в активном поиске (status=6).

    Args:
        user_info (dict): Результат "get_user_info".
        count (int): Сколько кандидатов вернуть (макс. 1000).
        offset (int): Смещение для пагинации.

    Returns:
        list[dict]: Список кандидатов. Каждый кандидат — словарь с полями
                    id, first_name, last_name, profile_link, age, city_title.
    """
    params = {
        'count': count,
        'offset': offset,
        'has_photo': 1,
        'status': 6,
    }

    sex = user_info.get('sex')
    if sex == 1:
        params['sex'] = 2
    elif sex == 2:
        params['sex'] = 1

    age = user_info.get('age')
    if age:
        params['age_from'] = age - 3
        params['age_to'] = age + 3

    city_id = user_info.get('city_id')
    if city_id:
        params['city'] = city_id

    response = vk.users.search(**params)
    items = response.get('items', [])

    candidates = []
    for item in items:
        candidates.append({
            'id': item.get('id'),
            'first_name': item.get('first_name'),
            'last_name': item.get('last_name'),
            'profile_link': f"https://vk.com/id{item.get('id')}",
            'age': None,
            'city_title': item.get('city', {}).get('title'),
        })

    return candidates


def get_candidate_with_photos(candidate):
    """
    Добавляет к кандидату список его топ-3 фотографий.

    Args:
        candidate (dict): Словарь кандидата из "search_candidates".

    Returns:
        dict: Тот же словарь с добавленным полем "top_photos" —
              списком фотографий (см. "get_top_photos").
    """
    candidate['top_photos'] = get_top_photos(candidate['id'])
    return candidate
