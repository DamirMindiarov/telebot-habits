import asyncio

from telebot.types import BotCommand

import handlers
from telebot import asyncio_filters

from loader import bot


async def main():
    # Add custom filters
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    # necessary for state parameter in handlers.
    from telebot.states.asyncio.middleware import StateMiddleware

    bot.setup_middleware(StateMiddleware(bot))
    await bot.set_my_commands([BotCommand("help", "помощь")])
    await bot.polling()


if __name__ == "__main__":
    asyncio.run(main())
