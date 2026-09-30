"""
Модуль для работы с фотографиями пользователей VK.

Содержит функцию "get_top_photos" — получение самых популярных
фотографий профиля по количеству лайков.
"""

from vk_service.auth import vk
from vk_service.utils import get_best_size


def get_top_photos(user_id, top_n=3):
    """
    Возвращает top_n самых популярных фотографий профиля.

    Популярность определяется по количеству лайков.
    Фотографии без лайков отбрасываются.

    Args:
        user_id (int): ID пользователя VK.
        top_n (int): Сколько фотографий вернуть (по умолчанию 3).

    Returns:
        list[dict]: Список фотографий. Каждая фотография — словарь с полями:
            - photo_id (int): ID фотографии;
            - owner_id (int): ID владельца;
            - likes (int): Количество лайков;
            - attachment (str): Строка для отправки в сообщении
              (формат "photo{owner_id}_{photo_id}");
            - url (str | None): Прямая ссылка на изображение.
    """
    response = vk.photos.get(
        owner_id=user_id,
        album_id='profile',
        extended=1,
        photo_sizes=1,
        count=50,
    )

    items = response.get('items', [])

    photo_with_likes = []
    for item in items:
        likes_count = item.get('likes', {}).get('count', 0)
        if likes_count > 0:
            photo_with_likes.append(item)

    photo_with_likes.sort(
        key=lambda item: item['likes']['count'],
        reverse=True,
    )

    top_photos = photo_with_likes[:top_n]

    result = []
    for photo in top_photos:
        owner_id = photo['owner_id']
        photo_id = photo['id']
        access_key = photo.get('access_key')

        attachment = f'photo{owner_id}_{photo_id}'
        if access_key:
            attachment += f'_{access_key}'

        result.append({
            'photo_id': photo_id,
            'owner_id': owner_id,
            'likes': photo['likes']['count'],
            'attachment': attachment,
            'url': get_best_size(photo.get('sizes', [])),
        })

    return result
