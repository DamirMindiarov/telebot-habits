import asyncio

from loader import bot
import handlers

if __name__ == '__main__':
    asyncio.run(bot.polling())
