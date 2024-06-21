from aiogram.filters.callback_data import CallbackData


class DateTimeSelectedCallback(CallbackData, prefix='date_time_selected'):
    date: str
    hours: int
    minutes: int
    utc: int
