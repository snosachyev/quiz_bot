import os
from dotenv import load_dotenv

load_dotenv()

# telegram bot token
API_TOKEN = os.getenv('API_TOKEN')

# Зададим имя базы данных
DB_NAME = os.getenv('DB_NAME')

# путь до файла с вопросами
QUIZ_DATA = os.getenv('QUIZ_DATA')

# list of telegram user id with admin`s permission
ADMIN_IDS = os.getenv('ADMIN_IDS').split(',')
