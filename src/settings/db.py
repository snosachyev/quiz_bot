import aiosqlite

from .config import DB_NAME


async def execute_async_db(sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
    async with aiosqlite.connect(DB_NAME) as db:
        # db.row_factory = aiosqlite.Row
        if not parameters:
            parameters = ()
        data = None
        cursor = await db.cursor()
        await cursor.execute(sql, parameters)

        if commit:
            await db.commit()

        if fetchone:
            data = await cursor.fetchone()
        if fetchall:
            data = await cursor.fetchall()
        return data
