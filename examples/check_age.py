"""Проверка функции calculate_age."""

from vk_service.utils import calculate_age

tests = [
    "15.03.1995",
    "15.03",
    None,
    "",
    "abc.def.ghi",
]

for t in tests:
    print(f"{t!r:20} → {calculate_age(t)}")
