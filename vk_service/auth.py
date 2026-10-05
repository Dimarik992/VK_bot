"""
Модуль авторизации в VK API.

Создаёт единый объект "vk" для всех модулей пакета.
Токен берётся из config (переменные окружения / файл ".env").
"""

import vk_api

from config import VK_USER_TOKEN

# Проверка, что токен задан
if not VK_USER_TOKEN or VK_USER_TOKEN.startswith('Вставь'):
    raise ValueError(
        'Токен VK не задан. Скопируй .env.example в .env '
        'и вставь свой токен.'
    )

# Создание сессии VK API
vk_session = vk_api.VkApi(token=VK_USER_TOKEN)

# Единый объект VK API для всех модулей пакета
vk = vk_session.get_api()
