import calendar
from datetime import date, datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram_calendar.schemas import SimpleCalAct, highlight, superscript


class CreateNoteCalendarCallback(SimpleCalendarCallback, prefix='create'):
    act: SimpleCalAct


class CreateNoteCalendar(SimpleCalendar):
    ignore_callback = CreateNoteCalendarCallback(act=SimpleCalAct.ignore).pack()  # placeholder for no answer buttons

    async def start_calendar(self, year: int = 2024, month: int = 8) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """

        today = datetime.now()
        now_weekday = self._labels.days_of_week[today.weekday()]
        now_month, now_year, now_day = today.month, today.year, today.day

        def highlight_month():
            month_str = self._labels.months[month - 1]
            if now_month == month and now_year == year:
                return highlight(month_str)
            return month_str

        def highlight_weekday():
            if now_month == month and now_year == year and now_weekday == weekday:
                return highlight(weekday)
            return weekday

        def format_day_string():
            date_to_check = datetime(year, month, day)
            if self.min_date and date_to_check < self.min_date:
                return superscript(str(day))
            elif self.max_date and date_to_check > self.max_date:
                return superscript(str(day))
            return str(day)

        def highlight_day():
            day_string = format_day_string()
            if now_month == month and now_year == year and now_day == day:
                return highlight(day_string)
            return day_string

        # building a calendar keyboard
        kb = []
        # today = datetime.now().date()

        # inline_kb = InlineKeyboardMarkup(row_width=7)
        # First row - Year
        years_row = []
        if date(year, month, 1) < today.date() or (month < today.month and year >= today.year):
            years_row.append(InlineKeyboardButton(text=' ', callback_data=self.ignore_callback))
        else:
            years_row.append(
                InlineKeyboardButton(
                    text='<<',
                    callback_data=CreateNoteCalendarCallback(
                        act=SimpleCalAct.prev_y, year=year, month=month, day=1
                    ).pack(),
                )
            )

        years_row.append(
            InlineKeyboardButton(
                text=str(year) if year != now_year else highlight(year), callback_data=self.ignore_callback
            )
        )
        years_row.append(
            InlineKeyboardButton(
                text='>>',
                callback_data=CreateNoteCalendarCallback(act=SimpleCalAct.next_y, year=year, month=month, day=1).pack(),
            )
        )
        kb.append(years_row)

        # Month nav Buttons
        month_row = []
        # (day != 0 and date(year, month, day) < today.date()
        if date(year, month, 1) < today.date():
            month_row.append(InlineKeyboardButton(text=' ', callback_data=self.ignore_callback))
        else:
            month_row.append(
                InlineKeyboardButton(
                    text='<',
                    callback_data=CreateNoteCalendarCallback(
                        act=SimpleCalAct.prev_m, year=year, month=month, day=1
                    ).pack(),
                )
            )

        month_row.append(InlineKeyboardButton(text=highlight_month(), callback_data=self.ignore_callback))
        month_row.append(
            InlineKeyboardButton(
                text='>',
                callback_data=CreateNoteCalendarCallback(act=SimpleCalAct.next_m, year=year, month=month, day=1).pack(),
            )
        )
        kb.append(month_row)

        # Week Days
        week_days_labels_row = []
        for weekday in self._labels.days_of_week:
            week_days_labels_row.append(
                InlineKeyboardButton(text=highlight_weekday(), callback_data=self.ignore_callback)
            )
        kb.append(week_days_labels_row)

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)

        for week in month_calendar:
            empty = 0
            days_row = []
            for day in week:
                if day == 0 or (day != 0 and date(year, month, day) < today.date()):
                    empty += 1
                    days_row.append(InlineKeyboardButton(text=' ', callback_data=self.ignore_callback))
                    continue
                days_row.append(
                    InlineKeyboardButton(
                        text=highlight_day(),
                        callback_data=CreateNoteCalendarCallback(
                            act=SimpleCalAct.day, year=year, month=month, day=day
                        ).pack(),
                    )
                )
            if empty < 7:
                kb.append(days_row)

        # nav today & cancel button
        cancel_row = []
        cancel_row.append(
            InlineKeyboardButton(
                text=self._labels.cancel_caption,
                callback_data=CreateNoteCalendarCallback(
                    act=SimpleCalAct.cancel, year=year, month=month, day=day
                ).pack(),
            )
        )
        cancel_row.append(InlineKeyboardButton(text=' ', callback_data=self.ignore_callback))
        cancel_row.append(
            InlineKeyboardButton(
                text=self._labels.today_caption,
                callback_data=CreateNoteCalendarCallback(
                    act=SimpleCalAct.today, year=year, month=month, day=day
                ).pack(),
            )
        )
        kb.append(cancel_row)
        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)
