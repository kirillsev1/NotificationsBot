import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.callbacks.notes.data.datetime import DateTimeSelectedCallback
from src.callbacks.notes.data.timepicker import TimePickerCallback


def create_button(text, hours, minutes, date_str, utc):
    button_datetime = datetime.datetime.combine(
        datetime.datetime.strptime(date_str, '%Y-%m-%d').date(), datetime.time(hours, minutes)
    )
    if button_datetime <= datetime.datetime.now() + datetime.timedelta(hours=utc):
        return InlineKeyboardButton(text=' ', callback_data='None')
    return InlineKeyboardButton(
        text=text, callback_data=TimePickerCallback(hours=hours, minutes=minutes, date=date_str, utc=utc).pack()
    )


def time_picker_keyboard(hours, minutes, date_str, utc=0):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                create_button('/\\', (hours + 1) % 24, minutes, date_str, utc),
                create_button('/\\', hours, (minutes + 1) % 60, date_str, utc),
                InlineKeyboardButton(
                    text='/\\',
                    callback_data=TimePickerCallback(
                        hours=hours + 1, minutes=minutes, date=date_str, utc=utc + 1
                    ).pack(),
                ),
            ],
            [
                create_button(f'{hours:02d}', hours, minutes, date_str, utc),
                create_button(f'{minutes:02d}', hours, minutes, date_str, utc),
                InlineKeyboardButton(text=f'{utc}', callback_data='None'),
            ],
            [
                create_button('\\/', (hours - 1) % 24, minutes, date_str, utc),
                create_button('\\/', hours, (minutes - 1) % 60, date_str, utc),
                InlineKeyboardButton(
                    text='\\/',
                    callback_data=TimePickerCallback(
                        hours=hours - 1, minutes=minutes, date=date_str, utc=utc - 1
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='done',
                    callback_data=DateTimeSelectedCallback(hours=hours, minutes=minutes, date=date_str, utc=utc).pack(),
                )
            ],
        ]
    )
