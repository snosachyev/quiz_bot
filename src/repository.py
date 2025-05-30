import aiosqlite

from settings.config import DB_NAME
from settings.db import execute_async_db


async def get_quiz_index(user_id):
    # Получаем запись для заданного пользователя
    sql = 'SELECT question_index FROM quiz_state WHERE user_id = (?)'
    # Возвращаем результат
    results = await execute_async_db(sql=sql, parameters=(user_id,), fetchone=True)
    if results is not None:
        return results[0]
    else:
        return 0


async def get_user_quiz_statistic(user_id):
    # Получаем статистику для заданного пользователя
    sql = (f'select count() as count_type_answers, question_index, result '
           f'from quiz_statistic '
           f'WHERE user_id = (?) GROUP BY question_index, result')
    return await execute_async_db(sql=sql, parameters=(user_id,), fetchall=True)


async def add_quiz_statistic(user_id, index, result):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    sql = (f'INSERT INTO quiz_statistic (user_id, question_index, result) VALUES'
           f' (?, ?, ?)')
    return await execute_async_db(sql=sql, parameters=(user_id, index, result), commit=True)


async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    sql = (f'INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES '
           f'(?, ?)')
    return await execute_async_db(sql=sql, parameters=(user_id, index), commit=True)


async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    sql = '''CREATE TABLE IF NOT EXISTS quiz_state
     (user_id INTEGER PRIMARY KEY, question_index INTEGER)'''
    await execute_async_db(sql=sql, commit=True)

    sql = '''CREATE TABLE IF NOT EXISTS quiz_statistic 
    (user_id INTEGER, question_index INTEGER, result INTEGER)'''
    await execute_async_db(sql=sql, commit=True)
