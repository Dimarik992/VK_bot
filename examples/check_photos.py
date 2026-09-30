"""Проверка функции get_top_photos."""

from vk_service.photos import get_top_photos

photos = get_top_photos(257879757)
for p in photos:
    print(p)
