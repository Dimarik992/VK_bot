"""Проверка функции get_user_info."""

from vk_service.users import get_user_info

info = get_user_info(257879757)
print(info)
