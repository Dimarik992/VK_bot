"""
Клиент VK API для бота.

Оборачивает vk_api: LongPoll, отправка сообщений и методы
для работы с пользователями через пользовательский токен.
"""

from typing import Any, Dict, Iterator, List, Optional

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from config import VK_GROUP_TOKEN
from vk_service.auth import vk
from vk_service.photos import get_top_photos
from vk_service.users import get_user_info


class VkClient:
    """
    Клиент для бота: слушает события Long Poll,
    отправляет сообщения и получает данные через API.
    """

    def __init__(self) -> None:
        if not VK_GROUP_TOKEN or VK_GROUP_TOKEN.startswith('Вставьте'):
            raise ValueError(
                'VK_GROUP_TOKEN не задан. Добавь его в .env — '
                'токен сообщества из настроек группы.'
            )

        self._bot_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
        self._bot_vk = self._bot_session.get_api()

        group_id = self._get_group_id()
        self._longpoll = VkBotLongPoll(self._bot_session, group_id)

    def _get_group_id(self) -> int:
        """Возвращает ID сообщества, которому принадлежит токен."""
        groups = self._bot_vk.groups.getById()
        if not groups:
            raise RuntimeError('Не удалось определить ID сообщества.')
        return abs(groups[0]['id'])

    # --- Long Poll --------------------------------------------------------
    def listen(self) -> Iterator:
        """Бесконечный генератор событий Long Poll."""
        for event in self._longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                yield event

    # --- отправка сообщений ----------------------------------------------
    def send_message(self, peer_id: int, text: str,
                     keyboard: Optional[str] = None,
                     attachment: Optional[str] = None) -> None:
        """Отправляет сообщение в диалог с пользователем."""
        params: Dict[str, Any] = {
            'peer_id': peer_id,
            'message': text,
            'random_id': 0,
        }
        if keyboard:
            params['keyboard'] = keyboard
        if attachment:
            params['attachment'] = attachment

        self._bot_vk.messages.send(**params)

    # --- данные пользователей --------------------------------------------
    def get_user_info(self, user_id: int) -> Dict[str, Any]:
        """Возвращает данные пользователя (пол, дата рождения, город)."""
        return get_user_info(user_id) or {}

    def get_city_id(self, city_name: str) -> Optional[int]:
        """
        Ищет ID города по названию через VK API.
        Возвращает None, если город не найден.
        """
        if not city_name:
            return None

        response = vk.database.getCities(
            q=city_name,
            count=1,
        )
        items = response.get('items', [])
        if not items:
            return None
        return items[0].get('id')

    def search_users(self, sex: int, age_from: int, age_to: int,
                     city_id: Optional[int] = None,
                     count: int = 50) -> List[Dict[str, Any]]:
        """
        Ищет пользователей по параметрам.
        Возвращает список словарей из VK API (users.search).
        """
        params: Dict[str, Any] = {
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'count': count,
            'has_photo': 1,
            'status': 6,
        }
        if city_id:
            params['city'] = city_id

        response = vk.users.search(**params)
        return response.get('items', [])

    def get_top_photos(self, user_id: int) -> List[Dict[str, Any]]:
        """Возвращает топ-3 фотографии пользователя по лайкам."""
        return get_top_photos(user_id)

