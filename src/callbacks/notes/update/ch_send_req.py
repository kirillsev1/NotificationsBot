from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from conf.config import settings
from src.callbacks.notes.inline_keyboards.notes_table import NoteSendCallbackData
from src.callbacks.notes.router import notes_callback_router
from src.utils.request import do_request


def update_button_text(
        table: InlineKeyboardMarkup, new_button: InlineKeyboardButton, callback_data: str
) -> InlineKeyboardMarkup:
    for row in table.inline_keyboard:
        for button_index, button in enumerate(row):
            if button.callback_data == callback_data:
                row[button_index] = new_button
                break
    return table


@notes_callback_router.callback_query(NoteSendCallbackData.filter())
async def update_send_required(
        callback_query: CallbackQuery,
        callback_data: NoteSendCallbackData,
        state: FSMContext
) -> None:
    if datetime.strptime(callback_data.datetime, '%Y-%m-%dT%H|%M|%SZ') <= datetime.utcnow():
        await callback_query.message.answer('note deactivated')
        return
    access_token = (await state.get_data()).get('access_token')
    current_keyboard = callback_query.message.reply_markup
    item_id = callback_data.note_id
    await do_request(
        f'{settings.BACKEND_HOST}/api/v1/note/send_required/{item_id}',
        {
            'send_required': str(not callback_data.send_required),
            'page': callback_data.page,
        },
        headers={'access-token': access_token},
        method='PATCH',
    )

    if current_keyboard:
        updated = InlineKeyboardButton(text=str(not callback_data.send_required), callback_data=callback_query.data)
        current_keyboard = update_button_text(current_keyboard, updated, callback_query.data)

        await callback_query.message.edit_reply_markup(reply_markup=current_keyboard)
