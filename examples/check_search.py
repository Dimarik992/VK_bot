"""Проверка функции search_candidates."""

from vk_service.users import get_user_info, search_candidates

info = get_user_info(257879757)
print("Инфо о клиенте:", info)
print()

candidates = search_candidates(info, count=10)
print(f"Найдено кандидатов: {len(candidates)}")
for c in candidates:
    print(c)
