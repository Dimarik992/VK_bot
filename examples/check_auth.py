"""Проверка авторизации в VK API."""

from vk_service.auth import vk

result = vk.users.get(user_ids=257879757, fields='sex, bdate, city')
print(result)
