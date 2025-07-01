#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot asosiy fayl
Aiogram 3.x va FSM ishlatilgan
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from data.config import BOT_TOKEN
from handlers.users.main.start import router as start_router
from handlers.users.admin.admin_panel import router as admin_router
from utils.database.db import init_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():

    # Bot va Dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)


    init_db()


    dp.include_router(start_router)
    dp.include_router(admin_router)

    logger.info("Bot ishga tushirilmoqda...")

    try:

        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi")
    except Exception as e:
        logger.error(f"Bot ishga tushirishda xatolik: {e}")