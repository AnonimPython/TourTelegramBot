import dotenv
import os
dotenv.load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import register_handlers
import asyncio



TOKEN = os.getenv("TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    register_handlers(dp)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())