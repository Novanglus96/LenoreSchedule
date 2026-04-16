import pytest
from datetime import date
from options.dto import DomainPayrollInfo, DomainPayrollInfoIn
from options.factories import PayrollInfoFactory
from options.models import PayrollInfo
from options.services.payroll_services import (
    create_payroll_info,
    update_payroll_info,
    get_payroll_info,
    get_ordered_list_of_payroll_infos,
    delete_payroll_info,
)
from options.exceptions import (
    PayrollInfoAlreadyExists,
    PayrollInfoDoesNotExist,
    PayrollInfoInvalidFirstDay,
    PayrollInfoInvalidSecondDay,
    PayrollInfoInvalidStart,
)


# ---------------------------------------------------------------------------
# create_payroll_info
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_success():
    """Creating a payroll_info should be successful and persistent."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="weekly",
    )

    result = create_payroll_info(dto)

    assert isinstance(result, DomainPayrollInfo)
    assert result.payroll_year == 2025
    assert result.payroll_frequency == "weekly"
    assert PayrollInfo.objects.filter(payroll_year=2025).exists()


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_start_in_prior_year_success():
    """A payroll start date in the prior year (e.g. Dec) should be accepted."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2024, 12, 29),
        payroll_frequency="weekly",
    )

    result = create_payroll_info(dto)

    assert result.payroll_year == 2025


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_duplicate_year_raises():
    """Creating a payroll_info with a duplicate year should raise PayrollInfoAlreadyExists."""
    PayrollInfoFactory(payroll_year=2025)
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="weekly",
    )

    with pytest.raises(PayrollInfoAlreadyExists):
        create_payroll_info(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_invalid_start_raises():
    """A payroll start date two years before the payroll year should raise PayrollInfoInvalidStart."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2023, 1, 1),
        payroll_frequency="weekly",
    )

    with pytest.raises(PayrollInfoInvalidStart):
        create_payroll_info(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_monthly_with_first_day_success():
    """Creating a monthly payroll_info with a valid first_day should succeed."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="monthly",
        first_day=15,
    )

    result = create_payroll_info(dto)

    assert result.payroll_frequency == "monthly"
    assert result.first_day == 15


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_monthly_without_first_day_raises():
    """Creating a monthly payroll_info without first_day should raise PayrollInfoInvalidFirstDay."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="monthly",
    )

    with pytest.raises(PayrollInfoInvalidFirstDay):
        create_payroll_info(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_semi_monthly_success():
    """Creating a semi-monthly payroll_info with valid days should succeed."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="semi-monthly",
        first_day=1,
        second_day=15,
    )

    result = create_payroll_info(dto)

    assert result.first_day == 1
    assert result.second_day == 15


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_semi_monthly_without_first_day_raises():
    """Creating a semi-monthly payroll_info without first_day should raise PayrollInfoInvalidFirstDay."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="semi-monthly",
        second_day=15,
    )

    with pytest.raises(PayrollInfoInvalidFirstDay):
        create_payroll_info(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_semi_monthly_without_second_day_raises():
    """Creating a semi-monthly payroll_info without second_day should raise PayrollInfoInvalidSecondDay."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="semi-monthly",
        first_day=1,
    )

    with pytest.raises(PayrollInfoInvalidSecondDay):
        create_payroll_info(dto)


@pytest.mark.django_db
@pytest.mark.service
def test_create_payroll_info_semi_monthly_second_day_lte_first_day_raises():
    """A semi-monthly second_day that is not greater than first_day should raise PayrollInfoInvalidSecondDay."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="semi-monthly",
        first_day=15,
        second_day=10,
    )

    with pytest.raises(PayrollInfoInvalidSecondDay):
        create_payroll_info(dto)


# ---------------------------------------------------------------------------
# update_payroll_info
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_update_payroll_info_success():
    """Updating a payroll_info should return an updated DomainPayrollInfo."""
    existing = PayrollInfoFactory(payroll_year=2024)
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="biweekly",
    )

    result = update_payroll_info(existing.id, dto)

    assert isinstance(result, DomainPayrollInfo)
    assert result.payroll_year == 2025
    assert result.payroll_frequency == "biweekly"


@pytest.mark.django_db
@pytest.mark.service
def test_update_payroll_info_same_year_success():
    """Updating a payroll_info without changing the year should succeed."""
    existing = PayrollInfoFactory(payroll_year=2025, payroll_frequency="weekly")
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="biweekly",
    )

    result = update_payroll_info(existing.id, dto)

    assert result.payroll_frequency == "biweekly"


@pytest.mark.django_db
@pytest.mark.service
def test_update_payroll_info_not_found_raises():
    """Updating a non-existent payroll_info should raise PayrollInfoDoesNotExist."""
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="weekly",
    )

    with pytest.raises(PayrollInfoDoesNotExist):
        update_payroll_info(99999, dto)


@pytest.mark.django_db
@pytest.mark.service
def test_update_payroll_info_duplicate_year_raises():
    """Updating a payroll_info to a year that already exists should raise PayrollInfoAlreadyExists."""
    PayrollInfoFactory(payroll_year=2025)
    existing = PayrollInfoFactory(payroll_year=2024)
    dto = DomainPayrollInfoIn(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="weekly",
    )

    with pytest.raises(PayrollInfoAlreadyExists):
        update_payroll_info(existing.id, dto)


# ---------------------------------------------------------------------------
# get_payroll_info
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_get_payroll_info_success():
    """Getting a payroll_info by id should return a DomainPayrollInfo."""
    existing = PayrollInfoFactory()

    result = get_payroll_info(existing.id)

    assert isinstance(result, DomainPayrollInfo)
    assert result.id == existing.id
    assert result.payroll_year == existing.payroll_year


@pytest.mark.django_db
@pytest.mark.service
def test_get_payroll_info_not_found_raises():
    """Getting a non-existent payroll_info should raise PayrollInfoDoesNotExist."""
    with pytest.raises(PayrollInfoDoesNotExist):
        get_payroll_info(99999)


# ---------------------------------------------------------------------------
# get_ordered_list_of_payroll_infos
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_get_ordered_list_of_payroll_infos_returns_domain_objects():
    """get_ordered_list_of_payroll_infos should return a list of DomainPayrollInfo objects."""
    PayrollInfoFactory(payroll_year=2024)
    PayrollInfoFactory(payroll_year=2025)

    result = get_ordered_list_of_payroll_infos()

    assert len(result) == 2
    assert all(isinstance(r, DomainPayrollInfo) for r in result)


@pytest.mark.django_db
@pytest.mark.service
def test_get_ordered_list_of_payroll_infos_empty():
    """get_ordered_list_of_payroll_infos should return an empty list when no records exist."""
    result = get_ordered_list_of_payroll_infos()

    assert result == []


@pytest.mark.django_db
@pytest.mark.service
def test_get_ordered_list_of_payroll_infos_ordered_descending():
    """get_ordered_list_of_payroll_infos should order by payroll_year descending."""
    PayrollInfoFactory(payroll_year=2023)
    PayrollInfoFactory(payroll_year=2025)
    PayrollInfoFactory(payroll_year=2024)

    result = get_ordered_list_of_payroll_infos()

    assert [r.payroll_year for r in result] == [2025, 2024, 2023]


# ---------------------------------------------------------------------------
# delete_payroll_info
# ---------------------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.service
def test_delete_payroll_info_success():
    """Deleting a payroll_info should remove it from the database and return the year."""
    existing = PayrollInfoFactory(payroll_year=2025)

    result = delete_payroll_info(existing.id)

    assert result == 2025
    assert not PayrollInfo.objects.filter(id=existing.id).exists()


@pytest.mark.django_db
@pytest.mark.service
def test_delete_payroll_info_not_found_raises():
    """Deleting a non-existent payroll_info should raise PayrollInfoDoesNotExist."""
    with pytest.raises(PayrollInfoDoesNotExist):
        delete_payroll_info(99999)
