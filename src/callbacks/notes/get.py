from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from src.callbacks.notes.data.pagination import PaginationCallback
from src.callbacks.notes.inline_keyboards.notes_table import get_notes_table
from src.callbacks.notes.router import notes_callback_router


@notes_callback_router.callback_query(SimpleCalendarCallback.filter())
async def handle_calendar(callback_query: CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext):
    calendar = SimpleCalendar()
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        date_str = date.strftime('%Y-%m-%d')
        await get_notes_table(callback_query, page=0, date=date_str, state=state)


@notes_callback_router.callback_query(PaginationCallback.filter())
async def handle_pagination(callback_query: CallbackQuery, callback_data: PaginationCallback, state: FSMContext):
    page = callback_data.page
    date = callback_data.date
    await get_notes_table(callback_query, page=page, date=date, state=state)
