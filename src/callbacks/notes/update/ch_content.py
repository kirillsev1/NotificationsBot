from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from conf.config import settings
from src.callbacks.notes.data.note import NoteContentCallbackData, UpdateNoteContentCallbackData
from src.callbacks.notes.router import notes_callback_router
from src.state.main import MainState
from src.utils.request import do_request


@notes_callback_router.callback_query(NoteContentCallbackData.filter())
async def get_content(callback_query: CallbackQuery, callback_data: NoteContentCallbackData, state: FSMContext):
    note = await do_request(
        f'{settings.BACKEND_HOST}/api/v1/note/{callback_data.note_id}',
        headers={'access-token': (await state.get_data()).get('access_token')},
        method='GET',
    )
    await callback_query.message.answer(
        note['content'],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='hide', callback_data='hide_content'),
                    InlineKeyboardButton(
                        text='update',
                        callback_data=UpdateNoteContentCallbackData(
                            note_id=callback_data.note_id, content=note['content'][:20], page=callback_data.page
                        ).pack(),
                    ),
                ]
            ]
        ),
    )


@notes_callback_router.callback_query(lambda callback: callback.data == 'hide_content')
async def hide_content(callback_query: CallbackQuery):
    await callback_query.message.delete()


@notes_callback_router.callback_query(UpdateNoteContentCallbackData.filter())
async def handel_content_update(
    callback_query: CallbackQuery, callback_data: UpdateNoteContentCallbackData, state: FSMContext
):
    await state.set_state(MainState.update_content)
    await state.update_data(
        {
            'update_note_id': callback_data.note_id,
            'update_msg_id': callback_query.message.message_id,
            'page': callback_data.page,
        }
    )
    await callback_query.message.edit_text(f'enter new text to replace:\n{callback_data.content}...')
    await callback_query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='cancel', callback_data='cancel')]]
        )
    )


@notes_callback_router.message(MainState.update_content)
async def update_content(message: Message, state: FSMContext):
    state_data = await state.get_data()
    access_token = state_data.get('access_token')
    note_id = state_data.get('update_note_id')
    page = state_data.get('page')
    await do_request(
        f'{settings.BACKEND_HOST}/api/v1/note/content/{note_id}',
        {
            'content': message.text,
            'offset': page * 10,
        },
        headers={'access-token': access_token},
        method='PATCH',
    )
    await state.set_state()
    await Bot(settings.BOT_TOKEN).delete_message(chat_id=message.chat.id, message_id=state_data.get('update_msg_id'))
    await message.answer(text='updated')
    await message.delete()
