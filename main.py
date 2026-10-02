#TODO  - поправить загрузку модулей
from bot.handlers import BotHandlers
from database.db_engine import init_db
from vk_service.vk_client import VkClient


def main():

    init_db()
    print("База данных готова")

    #TODO добавить инициализацию VK и вызов бота
    #vk = VkClient()
    #handlers = BotHandlers(vk)

    print("VKinder запущен, ждём сообщения...")
    handlers.run()


if __name__ == "__main__":
    main()
