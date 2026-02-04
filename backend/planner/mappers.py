from planner.dto import (
    DomainHoliday,
    DomainHolidayIn,
    DomainCalendarEntry,
    DomainCalendarEntryIn,
)
from planner.api.schemas.holiday import HolidayIn, HolidayOut
from planner.api.schemas.calendar_entry import (
    CalendarEntryIn,
    CalendarEntryOut,
)
from planner.models import Holiday, CalendarEntry
from staff.mappers import (
    domain_employee_to_schema,
    domain_location_to_schema,
    model_to_domain_employee,
    model_to_domain_location,
)


def domain_holiday_to_schema(
    holiday: DomainHoliday,
) -> HolidayOut:
    return HolidayOut(
        id=holiday.id,
        holiday_name=holiday.holiday_name,
        rule_type=holiday.rule_type,
        observed_rule=holiday.observed_rule,
        month=holiday.month,
        day=holiday.day,
        weekday=holiday.weekday,
        week=holiday.week,
    )


def schema_to_domain_holiday(schema: HolidayIn) -> DomainHolidayIn:
    return DomainHolidayIn(
        holiday_name=schema.holiday_name,
        rule_type=schema.rule_type,
        observed_rule=schema.observed_rule,
        month=schema.month,
        day=schema.day,
        weekday=schema.weekday,
        week=schema.week,
    )


def domain_holiday_to_model(dto: DomainHolidayIn) -> Holiday:
    return Holiday(
        holiday_name=dto.holiday_name,
        rule_type=dto.rule_type,
        observed_rule=dto.observed_rule,
        month=dto.month,
        day=dto.day,
        weekday=dto.weekday,
        week=dto.week,
    )


def model_to_domain_holiday(model: Holiday) -> DomainHoliday:
    return DomainHoliday(
        id=model.id,
        holiday_name=model.holiday_name,
        rule_type=model.rule_type,
        observed_rule=model.observed_rule,
        month=model.month,
        day=model.day,
        weekday=model.weekday,
        week=model.week,
    )


def domain_calendar_entry_to_schema(
    entry: DomainCalendarEntry,
) -> CalendarEntryOut:
    return CalendarEntryOut(
        id=entry.id,
        employee=domain_employee_to_schema(entry.employee),
        calendar_date=entry.calendar_date,
        start_time=entry.start_time,
        end_time=entry.end_time,
        confirmed=entry.confirmed,
        location=domain_location_to_schema(entry.location),
        hours=entry.hours,
    )


def schema_to_domain_calendar_entry(
    schema: CalendarEntryIn,
) -> DomainCalendarEntryIn:
    return DomainCalendarEntryIn(
        employee_id=schema.employee_id,
        calendar_date=schema.calendar_date,
        start_time=schema.start_time,
        end_time=schema.end_time,
        confirmed=schema.confirmed,
        location_id=schema.location_id,
    )


def domain_calendar_entry_to_model(dto: DomainCalendarEntryIn) -> CalendarEntry:
    return CalendarEntry(
        employee_id=dto.employee_id,
        calendar_date=dto.calendar_date,
        start_time=dto.start_time,
        end_time=dto.end_time,
        confirmed=dto.confirmed,
        location_id=dto.location_id,
    )


def model_to_domain_calendar_entry(model: CalendarEntry) -> DomainCalendarEntry:
    return DomainCalendarEntry(
        id=model.id,
        employee=model_to_domain_employee(model.employee),
        calendar_date=model.calendar_date,
        start_time=model.start_time,
        end_time=model.end_time,
        confirmed=model.confirmed,
        location=model_to_domain_location(model.location),
        hours=0,
    )
