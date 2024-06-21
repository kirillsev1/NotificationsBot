from datetime import datetime

from aiogram import F
from aiogram.types import Message
from aiogram_calendar import SimpleCalendar

from src.hendlers.notes.router import main_router


@main_router.message(F.text.lower() == 'navigation calendar w month')
async def nav_cal_handler_date(message: Message):
    calendar = SimpleCalendar()
    current_date = datetime.now()
    await message.answer(
        'Please select a date: ',
        reply_markup=await calendar.start_calendar(year=current_date.year, month=current_date.month),
    )
