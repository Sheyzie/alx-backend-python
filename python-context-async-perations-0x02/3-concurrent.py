# Async Context Manager Solution:
import asyncio
from contextlib import asynccontextmanager
import aiosqlite


async def async_connect():
    conn = await aiosqlite.connect('users_data.db')
    return conn


@asynccontextmanager
async def get_async_db_conn():
    conn = await async_connect()

    try:
        yield conn
    finally:
        await conn.close()

async def async_fetch_users():
    async with get_async_db_conn() as conn:
        cursor = await conn.cursor()
        await cursor.execute('SELECT * FROM users;')
        return await cursor.fetchall()

async def async_fetch_older_users():
    async with get_async_db_conn() as conn:
        cursor = await conn.cursor()
        await cursor.execute("SELECT * FROM users WHERE age > 40;")
        return await cursor.fetchall()
    
# Run concurrently
async def fetch_concurrently():
    users, older_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    print('User :', users)
    print('Older User :', older_users)
    return {"users": users, "older_users": older_users}

asyncio.run(fetch_concurrently())
