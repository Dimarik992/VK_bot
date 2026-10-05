import os
from dotenv import load_dotenv

load_dotenv()

# --- Подключение к БД ----------------------------------------------------
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# --- ВКонтакте -----------------------------------------------------------
VK_USER_TOKEN = os.getenv('VK_USER_TOKEN')
VK_GROUP_TOKEN = os.getenv('VK_GROUP_TOKEN')

# --- Настройки поиска ----------------------------------------------------
AGE_DELTA = 3  # ±3 года при поиске кандидатов
