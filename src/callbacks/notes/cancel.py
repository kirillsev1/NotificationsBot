from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar

from src.callbacks.notes.router import notes_callback_router


@notes_callback_router.callback_query(lambda callback: callback.data == 'cancel')
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state()
    calendar = SimpleCalendar()
    current_date = datetime.now()
    await callback_query.message.edit_text('Please select a date: ')
    await callback_query.message.edit_reply_markup(
        reply_markup=await calendar.start_calendar(year=current_date.year, month=current_date.month),
    )
