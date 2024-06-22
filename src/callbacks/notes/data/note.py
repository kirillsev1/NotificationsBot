from aiogram.filters.callback_data import CallbackData


class NoteCallbackData(CallbackData, prefix='note'):
    note_id: int


class NoteIdCallbackData(NoteCallbackData, prefix='note_id'):
    ...


class NoteContentCallbackData(NoteCallbackData, prefix='note_content'):
    page: int


class UpdateNoteContentCallbackData(NoteContentCallbackData, prefix='update_note_content'):
    content: str
    page: int


class NotePerformCallbackData(NoteCallbackData, prefix='note_perform'):
    ...


class NoteSendCallbackData(NoteCallbackData, prefix='note_send_required'):
    send_required: bool
    datetime: str
    page: int
