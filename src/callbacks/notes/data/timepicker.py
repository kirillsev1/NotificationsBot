from aiogram.filters.callback_data import CallbackData


class TimePickerCallback(CallbackData, prefix='timepicker'):
    date: str
    hours: int
    minutes: int
    utc: int
