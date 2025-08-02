from aiogram import types
from loader import dp

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Hello! Welcome to Top Study PDF Bot 😊\n\nUse /help to see available commands.")
