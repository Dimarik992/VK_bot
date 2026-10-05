"""Вспомогательные функции бота: тексты сообщений."""
from typing import Any, Dict

GENDER_TITLES = {1: "женский", 2: "мужской"}


def format_candidate_message(candidate: Dict[str, Any]) -> str:
    """Формирует текст сообщения с информацией о кандидате."""
    full_name = " ".join(
        part for part in (candidate.get("name"), candidate.get("last_name"))
        if part
    )
    link = candidate.get("profile_link")
    if not link:
        link = f"https://vk.com/id{candidate.get('vk_id')}"
    return f"{full_name}\n{link}"


def format_search_params(user, age_from: int, age_to: int, sex: int) -> str:
    """Формирует текст с параметрами предстоящего поиска."""
    gender = GENDER_TITLES.get(sex, "любой")
    city = user.city or "любой"
    return (
        "Параметры поиска:\n"
        f"• пол: {gender}\n"
        f"• город: {city}\n"
        f"• возраст: от {age_from} до {age_to}"
    )
