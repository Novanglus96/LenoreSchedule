import pytest
from staff.services.holiday_services import (
    create_holiday,
    update_holiday,
    get_holiday,
    get_ordered_list_of_holidays,
    delete_holiday,
)
from staff.dto import DomainHolidayIn, DomainHoliday
from staff.exceptions import HolidayAlreadyExists, HolidayDoesNotExist
from staff.models import Holiday


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
