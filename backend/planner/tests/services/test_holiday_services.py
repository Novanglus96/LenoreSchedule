import pytest
from planner.services.holiday_services import (
    create_holiday,
    update_holiday,
    get_holiday,
    get_ordered_list_of_holidays,
    delete_holiday,
    get_holiday_date_for_year,
)
from planner.dto import DomainHolidayIn, DomainHoliday
from planner.exceptions import (
    HolidayAlreadyExists,
    HolidayDoesNotExist,
    HolidayInvalidDayError,
    HolidayInvalidObservedRuleError,
    HolidayInvalidRuleError,
    HolidayInvalidWeekDayError,
    HolidayInvalidWeekError,
    HolidayInvalidMonthError,
)
from planner.models import Holiday
from datetime import date


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_success():
    """
    Creating a holiday should be successful and persistent.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="none",
        month=1,
        day=1,
        weekday=0,
        week=1,
    )

    holiday = create_holiday(dto)

    assert holiday.holiday_name == "Holiday"
    assert Holiday.objects.filter(holiday_name="Holiday").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_optional_fields():
    """
    Creating a holiday should be successful with optional fields.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="none",
    )

    holiday = create_holiday(dto)

    assert holiday.month is None
    assert holiday.day is None
    assert holiday.weekday is None
    assert holiday.week is None
    assert Holiday.objects.filter(holiday_name="Holiday").exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_duplicate_name_raises():
    """
    Creating a holiday with a duplciate holiday name should raise an error.
    """
    Holiday.objects.create(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="none",
        month=1,
        day=1,
        weekday=0,
        week=1,
    )

    with pytest.raises(HolidayAlreadyExists):
        create_holiday(
            DomainHolidayIn(
                holiday_name="Holiday",
                rule_type="fixed_date",
                observed_rule="none",
                month=1,
                day=1,
                weekday=0,
                week=1,
            )
        )


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_invalid_rule_raises():
    """
    Creating a holiday should raise an error with invalid rule.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="non_rule",
        observed_rule="none",
        month=1,
        day=1,
        weekday=0,
        week=1,
    )

    with pytest.raises(HolidayInvalidRuleError) as exc:
        create_holiday(dto)

    assert "non_rule" in str(exc.value)


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_invalid_month_raises():
    """
    Creating a holiday should raise an error with invalid month.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="none",
        month=13,
        day=1,
        weekday=0,
        week=1,
    )

    with pytest.raises(HolidayInvalidMonthError):
        create_holiday(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_invalid_day_raises():
    """
    Creating a holiday should raise an error with invalid day.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="none",
        month=1,
        day=32,
        weekday=0,
        week=1,
    )

    with pytest.raises(HolidayInvalidDayError):
        create_holiday(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_invalid_weekday_raises():
    """
    Creating a holiday should raise an error with invalid weekday.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="none",
        month=1,
        day=1,
        weekday=8,
        week=1,
    )

    with pytest.raises(HolidayInvalidWeekDayError):
        create_holiday(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_invalid_week_raises():
    """
    Creating a holiday should raise an error with invalid week.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="none",
        month=1,
        day=1,
        weekday=0,
        week=6,
    )

    with pytest.raises(HolidayInvalidWeekError):
        create_holiday(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_invalid_observed_rule_raises():
    """
    Creating a holiday should raise an error with invalid observed rule.
    """
    dto = DomainHolidayIn(
        holiday_name="Holiday",
        rule_type="fixed_date",
        observed_rule="non_rule",
        month=1,
        day=1,
        weekday=0,
        week=1,
    )

    with pytest.raises(HolidayInvalidObservedRuleError) as exc:
        create_holiday(dto)

    assert "non_rule" in str(exc.value)


@pytest.mark.django_db
@pytest.mark.service
def test_create_holiday_dto():
    """
    Creating a holiday should return a DomainHoliday object
    """
    holiday = create_holiday(
        DomainHolidayIn(
            holiday_name="Holiday",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )
    assert isinstance(holiday, DomainHoliday)


@pytest.mark.django_db
@pytest.mark.service
def test_update_holiday_success():
    """
    Updating a holiday should be successfull and persistent.
    """
    holiday = create_holiday(
        DomainHolidayIn(
            holiday_name="Holiday",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )

    updated = update_holiday(
        holiday_id=holiday.id,
        dto=DomainHolidayIn(
            holiday_name="Updated",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        ),
    )

    assert updated.holiday_name == "Updated"
    assert Holiday.objects.get(id=holiday.id).holiday_name == "Updated"


@pytest.mark.django_db
@pytest.mark.service
def test_update_holiday_duplicate_name_raises():
    """
    Updating a holiday with a duplciate holiday name should raise an error.
    """
    holiday = create_holiday(
        DomainHolidayIn(
            holiday_name="Holiday",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )
    create_holiday(
        DomainHolidayIn(
            holiday_name="Test",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )

    with pytest.raises(HolidayAlreadyExists):
        update_holiday(
            holiday.id,
            DomainHolidayIn(
                holiday_name="Test",
                rule_type="fixed_date",
                observed_rule="none",
                month=1,
                day=1,
                weekday=0,
                week=1,
            ),
        )


@pytest.mark.django_db
@pytest.mark.service
def test_update_holiday_not_found():
    """
    Upading a holiday that doesn't exist should raise an error.
    """
    with pytest.raises(HolidayDoesNotExist):
        update_holiday(
            999,
            DomainHolidayIn(
                holiday_name="Holiday",
                rule_type="fixed_date",
                observed_rule="none",
                month=1,
                day=1,
                weekday=0,
                week=1,
            ),
        )


@pytest.mark.django_db
@pytest.mark.service
def test_update_holiday_dto():
    """
    Updating a holiday should return a DomainHoliday
    """
    holiday = create_holiday(
        DomainHolidayIn(
            holiday_name="Holiday",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )

    updated = update_holiday(
        holiday_id=holiday.id,
        dto=DomainHolidayIn(
            holiday_name="Updated",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        ),
    )

    assert isinstance(updated, DomainHoliday)


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_dto():
    """
    Getting a holiday should return a DomainHoliday.
    """
    created_holiday = create_holiday(
        DomainHolidayIn(
            holiday_name="Holiday",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )

    holiday = get_holiday(created_holiday.id)
    assert isinstance(holiday, DomainHoliday)


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_not_found_raises():
    """
    Getting a holiday that doesn't exist should raise error.
    """
    with pytest.raises(HolidayDoesNotExist):
        get_holiday(999)


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_list():
    """
    Getting a list of holidays should return a list of DomainHolidays.
    """
    create_holiday(
        DomainHolidayIn(
            holiday_name="Easter",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )
    create_holiday(
        DomainHolidayIn(
            holiday_name="President's Day",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )
    create_holiday(
        DomainHolidayIn(
            holiday_name="Christmas",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )

    holidays = get_ordered_list_of_holidays()

    assert isinstance(holidays, list)
    assert holidays  # not empty
    assert all(isinstance(g, DomainHoliday) for g in holidays)


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_list_is_ordered():
    """
    Getting a list of holidays should return a list of DomainHolidays
    sorted ascending by holiday_name
    """
    create_holiday(
        DomainHolidayIn(
            holiday_name="Easter",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )
    create_holiday(
        DomainHolidayIn(
            holiday_name="President's Day",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )
    create_holiday(
        DomainHolidayIn(
            holiday_name="Christmas",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )

    holidays = get_ordered_list_of_holidays()

    names = [g.holiday_name for g in holidays]
    assert names == ["Christmas", "Easter", "President's Day"]


@pytest.mark.django_db
@pytest.mark.service
def test_delete_holiday_success():
    """
    Deleting the holiday should remove the holiday and return the holiday_name
    """
    holiday = create_holiday(
        DomainHolidayIn(
            holiday_name="Holiday",
            rule_type="fixed_date",
            observed_rule="none",
            month=1,
            day=1,
            weekday=0,
            week=1,
        )
    )

    deleted_holiday = delete_holiday(holiday.id)

    assert not Holiday.objects.filter(holiday_name="Holiday").exists()
    assert deleted_holiday == "Holiday"


@pytest.mark.django_db
@pytest.mark.service
def test_delete_holiday_not_found_raises():
    """
    Deleting a holiday that does not exist should raise an error.
    """
    with pytest.raises(HolidayDoesNotExist):
        delete_holiday(999)


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_fixed_observation_none():
    """
    Test holiday date is return correctly for fixed dates with
    no observation rule.
    """
    dto = DomainHolidayIn(
        holiday_name="Some Holiday",
        rule_type="fixed_date",
        observed_rule="none",
        month=7,
        day=4,
        weekday=0,
        week=1,
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 7, 4),
        "observed": False,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_fixed_observation_next_weekday_sat():
    """
    Test holiday date is return correctly for fixed dates with
    nearest weekday observation rule, falling on a saturday.
    """
    dto = DomainHolidayIn(
        holiday_name="Some Holiday",
        rule_type="fixed_date",
        observed_rule="nearest_weekday",
        month=7,
        day=4,
        weekday=0,
        week=1,
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 7, 3),
        "observed": True,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_fixed_observation_next_weekday_sun():
    """
    Test holiday date is return correctly for fixed dates with
    nearest weekday observation rule, falling on a sunday.
    """
    dto = DomainHolidayIn(
        holiday_name="Some Holiday",
        rule_type="fixed_date",
        observed_rule="nearest_weekday",
        month=7,
        day=5,
        weekday=0,
        week=1,
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 7, 6),
        "observed": True,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_fixed_observation_next_business_day_sat():
    """
    Test holiday date is return correctly for fixed dates with
    next business day observation rule, falling on a saturday.
    """
    dto = DomainHolidayIn(
        holiday_name="Some Holiday",
        rule_type="fixed_date",
        observed_rule="next_business_day",
        month=7,
        day=4,
        weekday=0,
        week=1,
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 7, 6),
        "observed": True,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_fixed_observation_next_business_day_sun():
    """
    Test holiday date is return correctly for fixed dates with
    next business day observation rule, falling on a sunday.
    """
    dto = DomainHolidayIn(
        holiday_name="Some Holiday",
        rule_type="fixed_date",
        observed_rule="next_business_day",
        month=7,
        day=5,
        weekday=0,
        week=1,
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 7, 6),
        "observed": True,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_nth_weekday():
    """
    Test holiday date is return correctly for nth weekday.
    """
    dto = DomainHolidayIn(
        holiday_name="Some Holiday",
        rule_type="nth_weekday",
        observed_rule="none",
        month=11,
        day=0,
        weekday=3,
        week=4,
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 11, 26),
        "observed": False,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_custom_easter():
    """
    Test holiday date is return correctly for custom date (easter).
    """
    dto = DomainHolidayIn(
        holiday_name="Easter Sunday",
        rule_type="custom",
        observed_rule="none",
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 4, 5),
        "observed": False,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_custom_good_friday():
    """
    Test holiday date is return correctly for custom date (good friday).
    """
    dto = DomainHolidayIn(
        holiday_name="Good Friday",
        rule_type="custom",
        observed_rule="none",
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 4, 3),
        "observed": False,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_custom_election_day():
    """
    Test holiday date is return correctly for custom date (election day).
    """
    dto = DomainHolidayIn(
        holiday_name="Election Day",
        rule_type="custom",
        observed_rule="none",
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 11, 3),
        "observed": False,
    }

    assert holiday_date == expected


@pytest.mark.django_db
@pytest.mark.service
def test_get_holiday_date_last_week_day():
    """
    Test holiday date is return correctly for last week day of month.
    """
    dto = DomainHolidayIn(
        holiday_name="Election Day",
        rule_type="last_weekday",
        observed_rule="none",
        month=3,
        weekday=3,
    )

    holiday = create_holiday(dto)

    holiday_date = get_holiday_date_for_year(holiday.id, 2026)
    expected = {
        "holiday_name": holiday.holiday_name,
        "holiday_date": date(2026, 3, 26),
        "observed": False,
    }

    assert holiday_date == expected
