import asyncio
import handlers
from telebot import asyncio_filters

from loader import bot

if __name__ == '__main__':
    # Add custom filters
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    # necessary for state parameter in handlers.
    from telebot.states.asyncio.middleware import StateMiddleware

    bot.setup_middleware(StateMiddleware(bot))

    asyncio.run(bot.polling())
