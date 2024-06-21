import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from conf.config import settings
from src.calendars.create_note_calendar import CreateNoteCalendar, CreateNoteCalendarCallback
from src.callbacks.notes.inline_keyboards.timepicker import time_picker_keyboard
from src.callbacks.notes.router import notes_callback_router
from src.utils.request import do_request


@notes_callback_router.callback_query(lambda callback: callback.data == 'create_note')
async def create_note(callback_query: CallbackQuery):
    await callback_query.message.edit_text('Please select a date:')
    calendar = CreateNoteCalendar()
    current_date = datetime.datetime.now()

    await callback_query.message.edit_reply_markup(
        reply_markup=await calendar.start_calendar(year=current_date.year, month=current_date.month),
    )


@notes_callback_router.callback_query(CreateNoteCalendarCallback.filter())
async def update_create_calendar(callback_query: CallbackQuery, callback_data: CreateNoteCalendarCallback, state: FSMContext):
    calendar = CreateNoteCalendar(show_alerts=True)
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        access_token = (await state.get_data()).get('access_token')
        date_str = date.strftime('%Y-%m-%d')
        utc = await do_request(
            f'{settings.BACKEND_HOST}/api/v1/note/utc',
            headers={
                'access-token': access_token
            },
            method='GET'
        )
        now = datetime.datetime.now()
        kb = time_picker_keyboard(hours=(now + datetime.timedelta(hours=utc['utc'])).hour, minutes=(now + datetime.timedelta(minutes=1)).minute, date_str=date_str, utc=utc['utc'])
        await callback_query.message.edit_text('Please select a time')
        await callback_query.message.edit_reply_markup(reply_markup=kb)
