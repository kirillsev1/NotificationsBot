import datetime
from math import floor

import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from conf.config import settings
from src.callbacks.notes.data.note import (
    NoteContentCallbackData,
    NoteIdCallbackData,
    NotePerformCallbackData,
    NoteSendCallbackData,
)
from src.callbacks.notes.header import get_header
from src.callbacks.notes.inline_keyboards.pagination import get_pagination
from src.utils.request import do_request

VIEW_FIELDS = ['id', 'content', 'time', 'send_required']


async def create_notes_table(
    notes: list[dict[str, any]], page: int, date: str, total_rows: int, state: FSMContext
) -> InlineKeyboardMarkup:
    notes_table = [[InlineKeyboardButton(text=field, callback_data=field) for field in VIEW_FIELDS]]
    total_pages = floor(total_rows / 10)
    utc = await do_request(
        f'{settings.BACKEND_HOST}/api/v1/user/utc',
        headers={'access-token': (await state.get_data()).get('access_token')},
        method='GET',
    )
    for item in notes:
        test = (datetime.datetime.fromisoformat(item.get('perform')) + datetime.timedelta(hours=utc['utc'])).isoformat()
        note = [
            InlineKeyboardButton(
                text=str(item.get('id')), callback_data=NoteIdCallbackData(note_id=item.get('id')).pack()
            ),
            InlineKeyboardButton(
                text=item.get('content')[:10],
                callback_data=NoteContentCallbackData(note_id=item.get('id'), page=page).pack(),
            ),
            InlineKeyboardButton(
                text=str(test.split('T')[1])[:-4][:-2],
                callback_data=NotePerformCallbackData(note_id=item.get('id')).pack(),
            ),
            InlineKeyboardButton(
                text=str(item.get('send_required')),
                callback_data=NoteSendCallbackData(
                    note_id=item.get('id'),
                    send_required=item.get('send_required'),
                    datetime=item.get('perform').replace(':', '|'),
                    page=page,
                ).pack(),
            ),
        ]
        notes_table.append(note)
    notes_table.append(await get_pagination(page, total_pages, date))
    notes_table += await get_header(page, date)
    return InlineKeyboardMarkup(inline_keyboard=notes_table)


async def get_notes_table(callback_query: CallbackQuery, page: int, date: str, state: FSMContext):
    access_token = (await state.get_data()).get('access_token')
    await state.update_data({'selected_date': date})

    try:
        notes = await do_request(
            f'{settings.BACKEND_HOST}/api/v1/note',
            params={
                'notes_date': date,
                'limit': 10,
                'offset': page * 10
            },
            headers={'access-token': access_token},
            method='GET',
        )
    except aiohttp.ClientResponseError:
        await callback_query.message.edit_text('Notes were not found')
        await callback_query.message.edit_reply_markup(
            reply_markup=InlineKeyboardMarkup(inline_keyboard=await get_header(page, date))
        )
    else:
        await callback_query.message.edit_text(text=f'Notes for {date.split("T")[0]}:')
        table = await create_notes_table(notes['notes'], page, date, notes['total_rows'], state)
        await callback_query.message.edit_reply_markup(reply_markup=table)
