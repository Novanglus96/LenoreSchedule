class HolidayAlreadyExists(Exception):
    pass


class HolidayCreationError(Exception):
    pass


class HolidayDoesNotExist(Exception):
    def __init__(self, holiday_id: int):
        super().__init__(f"Holiday {holiday_id} does not exist")
        self.holiday_id = holiday_id


class HolidayInvalidRuleError(Exception):
    pass


class HolidayInvalidMonthError(Exception):
    pass


class HolidayInvalidDayError(Exception):
    pass


class HolidayInvalidWeekDayError(Exception):
    pass


class HolidayInvalidWeekError(Exception):
    pass


class HolidayInvalidObservedRuleError(Exception):
    pass


class CalendarEntryAlreadyExists(Exception):
    pass


class CalendarEntryCreationError(Exception):
    pass


class CalendarEntryDoesNotExist(Exception):
    def __init__(self, calendar_entry_id: int):
        super().__init__(f"Calendar Entry {calendar_entry_id} does not exist")
        self.calendar_entry_id = calendar_entry_id
