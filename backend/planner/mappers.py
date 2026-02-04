from planner.dto import (
    DomainHoliday,
    DomainHolidayIn,
)
from planner.api.schemas.holiday import HolidayIn, HolidayOut
from planner.models import Holiday


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
