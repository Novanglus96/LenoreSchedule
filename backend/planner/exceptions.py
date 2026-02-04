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
