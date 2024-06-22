from aiogram.types import CallbackQuery

from src.callbacks.notes.data.timepicker import TimePickerCallback
from src.callbacks.notes.inline_keyboards.timepicker import time_picker_keyboard
from src.callbacks.notes.router import notes_callback_router


@notes_callback_router.callback_query(TimePickerCallback.filter())
async def get_time(callback_query: CallbackQuery, callback_data: TimePickerCallback):
    hours = callback_data.hours
    minutes = callback_data.minutes
    date_str = callback_data.date
    utc = callback_data.utc
    kb = time_picker_keyboard(hours=hours, minutes=minutes, date_str=date_str, utc=utc)
    await callback_query.message.edit_reply_markup(reply_markup=kb)
