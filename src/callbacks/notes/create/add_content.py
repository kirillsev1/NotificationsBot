import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from conf.config import settings
from src.callbacks.notes.data.pagination import PaginationCallback
from src.callbacks.notes.router import notes_callback_router
from src.state.main import MainState
from src.utils.request import do_request


@notes_callback_router.message(MainState.add_content)
async def add_content(message: Message, state: FSMContext):
    access_token = (await state.get_data()).get('access_token')
    note_perform_data = (await state.get_data())['note']
    note_perform = datetime.datetime.combine(
        datetime.datetime.strptime(note_perform_data['date'], '%Y-%m-%d').date(),
        datetime.time(note_perform_data['hours'], note_perform_data['minutes']),
    )
    await do_request(
        f'{settings.BACKEND_HOST}/api/v1/note',
        body={'perform': note_perform.isoformat(), 'content': message.text, 'send_required': 'true'},
        headers={'access-token': access_token},
    )
    await state.set_state()

    await message.answer(
        'created successfully',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='to date', callback_data=PaginationCallback(page=0, date=note_perform_data['date']).pack()
                    )
                ]
            ]
        ),
    )
