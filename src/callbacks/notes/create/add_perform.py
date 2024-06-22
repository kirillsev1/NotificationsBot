import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from conf.config import settings
from src.callbacks.notes.data.datetime import DateTimeSelectedCallback
from src.callbacks.notes.inline_keyboards.timepicker import time_picker_keyboard
from src.callbacks.notes.router import notes_callback_router
from src.state.main import MainState
from src.utils.request import do_request


@notes_callback_router.callback_query(DateTimeSelectedCallback.filter())
async def add_perform(callback_query: CallbackQuery, callback_data: DateTimeSelectedCallback, state: FSMContext):
    button_datetime = datetime.datetime.combine(
        datetime.datetime.strptime(callback_data.date, '%Y-%m-%d').date(),
        datetime.time(callback_data.hours, callback_data.minutes)
    )
    now = datetime.datetime.now()

    if button_datetime <= datetime.datetime.now() + datetime.timedelta(hours=callback_data.utc):
        kb = time_picker_keyboard(
            hours=(now + datetime.timedelta(hours=callback_data.utc)).hour,
            minutes=(now + datetime.timedelta(minutes=1)).minute,
            date_str=callback_data.date,
            utc=callback_data.utc
        )
        await callback_query.message.edit_text('Please select a time')
        await callback_query.message.edit_reply_markup(reply_markup=kb)
        return

    selected = button_datetime - datetime.timedelta(hours=callback_data.utc)
    await state.update_data(
        {
            'note': {
                'date': selected.date().strftime('%Y-%m-%d'),
                'hours': selected.hour,
                'minutes': selected.minute
            }
        }
    )

    await do_request(
        f'{settings.BACKEND_HOST}/api/v1/user/utc',
        params={
            'utc': callback_data.utc
        },
        headers={
            'access-token': (await state.get_data()).get('access_token')
        },
        method='PATCH'
    )
    await state.set_state(MainState.add_content)
    await callback_query.message.answer('enter content')
