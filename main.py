import logging
import os
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher


from bot.database.models import database_main
from bot.routers.main_router import main_router
from bot.routers.item_router import item_router


load_dotenv()


async def main():
    await database_main()
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(item_router)
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
