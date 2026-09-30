"""
Модуль авторизации в VK API.

Создаёт единый объект "vk" для всех модулей пакета.
Токен берётся из переменных окружения (файл ".env").
"""

import os

import vk_api
from dotenv import load_dotenv

load_dotenv()

VK_USER_TOKEN = os.getenv('VK_USER_TOKEN')

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
