from aiogram import Bot
from aiogram.enums import ParseMode

from conf.config import settings

bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
