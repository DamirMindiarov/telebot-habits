from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from config import TOKEN

bot = AsyncTeleBot(token=TOKEN, state_storage=StateMemoryStorage())
