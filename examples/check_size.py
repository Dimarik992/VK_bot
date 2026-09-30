"""Проверка функции get_best_size."""

from vk_service.utils import get_best_size

print(get_best_size([
    {'type': 'm', 'url': 'url_m'},
    {'type': 'x', 'url': 'url_x'},
    {'type': 'z', 'url': 'url_z'},
]))

print(get_best_size([
    {'type': 'm', 'url': 'url_m'},
    {'type': 's', 'url': 'url_s'},
]))

print(get_best_size([]))
print(get_best_size(None))
