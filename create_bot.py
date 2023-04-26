from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
#create bot
TOKEN = ""
with open('token.txt') as file:
    TOKEN: str = file.readline()
bot = Bot(TOKEN)
dp = Dispatcher(bot)
