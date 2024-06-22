from aiogram.types import InlineKeyboardButton

from src.callbacks.notes.data.pagination import PaginationCallback


async def get_pagination(page, total_pages, date):
    pagination_buttons = [
        InlineKeyboardButton(text=str(page), callback_data=PaginationCallback(page=page, date=date).pack()),
    ]

    if total_pages <= 1:
        pagination_buttons.insert(
            0,
            InlineKeyboardButton(text=' ', callback_data=PaginationCallback(page=page, date=date).pack()),
        )
        pagination_buttons.append(
            InlineKeyboardButton(text=' ', callback_data=PaginationCallback(page=page, date=date).pack()),
        )
        return pagination_buttons

    prev_page = total_pages - 1 if page == 0 else page - 1
    next_page = 0 if page == total_pages - 1 else page + 1

    pagination_buttons.insert(
        0,
        InlineKeyboardButton(text='<<', callback_data=PaginationCallback(page=prev_page, date=date).pack()),
    )
    pagination_buttons.append(
        InlineKeyboardButton(text='>>', callback_data=PaginationCallback(page=next_page, date=date).pack()),
    )

    return pagination_buttons
