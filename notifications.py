import asyncio
import time

from sqlalchemy import select
from telebot.async_telebot import AsyncTeleBot

from bot.loader import bot
from app.database import session_async, UsersDB
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def get_users_id():
    async with session_async() as session:
        users_id = await session.execute(select(UsersDB.user_id))

    return users_id.scalars().fetchall()


async def myfunc(my_bot: AsyncTeleBot):
    users_id = await get_users_id()

    for user_id in users_id:
        await my_bot.send_message(chat_id=int(user_id), text="Privet")


async def main():
    scheduler.add_job(myfunc,
                      'interval',
                      seconds=2,
                      id='my_job_id',
                      kwargs={'my_bot': bot}
                      )
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == "__main__":
    asyncio.run(main())
