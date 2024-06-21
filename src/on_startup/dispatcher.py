from aiogram import Bot, Dispatcher

from src.callbacks.notes.router import notes_callback_router
from src.hendlers.auth.router import auth_router
from src.hendlers.notes.router import main_router
from src.middlewares.auth import AuthMiddleware
from src.middlewares.logger import LogMessageMiddleware


def setup_dispatcher(bot: Bot) -> Dispatcher:
    dp = Dispatcher(bot=bot)

    dp.include_router(main_router)
    dp.include_router(notes_callback_router)
    dp.include_router(auth_router)

    dp.message.middleware(LogMessageMiddleware())
    dp.callback_query.middleware(LogMessageMiddleware())

    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    return dp
