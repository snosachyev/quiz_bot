import asyncio
import logging
from aiogram import Bot, Dispatcher


from settings.config import API_TOKEN
from db import create_table
from routers import quiz_router

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

dp.include_router(quiz_router)


# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
