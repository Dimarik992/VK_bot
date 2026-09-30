"""Полная проверка: кандидаты + их топ-3 фото."""

from vk_service.users import (
    get_user_info,
    search_candidates,
    get_candidate_with_photos,
)

info = get_user_info(257879757)
candidates = search_candidates(info, count=3)

for c in candidates:
    full = get_candidate_with_photos(c)
    print(f"{full['first_name']} {full['last_name']}")
    print(f"Ссылка: {full['profile_link']}")
    print(f"Фото: {len(full['top_photos'])} шт.")
    for photo in full['top_photos']:
        print(f"  - {photo['attachment']} (лайков: {photo['likes']})")
    print('---')
