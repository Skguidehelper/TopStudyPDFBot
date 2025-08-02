# loader.py
from config import TOKEN

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
