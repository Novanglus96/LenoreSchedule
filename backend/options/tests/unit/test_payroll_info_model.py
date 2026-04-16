import pytest
from datetime import date
from django.db import IntegrityError
from options.models import PayrollInfo


@pytest.mark.django_db
@pytest.mark.unit
def test_payroll_info_creation():
    """Test PayrollInfo is created successfully with all fields."""
    payroll_info = PayrollInfo.objects.create(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="weekly",
    )

    assert payroll_info.id is not None
    assert payroll_info.payroll_year == 2025
    assert payroll_info.payroll_start == date(2025, 1, 1)
    assert payroll_info.payroll_frequency == "weekly"
    assert payroll_info.first_day is None
    assert payroll_info.second_day is None


@pytest.mark.django_db
@pytest.mark.unit
def test_payroll_info_creation_with_optional_days():
    """Test PayrollInfo is created successfully with first_day and second_day."""
    payroll_info = PayrollInfo.objects.create(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="semi-monthly",
        first_day=1,
        second_day=15,
    )

    assert payroll_info.first_day == 1
    assert payroll_info.second_day == 15


@pytest.mark.django_db
@pytest.mark.unit
def test_payroll_info_string_representation():
    """Test __str__ returns the payroll year as a string."""
    payroll_info = PayrollInfo.objects.create(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="weekly",
    )

    assert str(payroll_info) == "2025"


@pytest.mark.django_db
@pytest.mark.unit
def test_payroll_info_year_unique_constraint():
    """Test that duplicate payroll_year raises an IntegrityError."""
    PayrollInfo.objects.create(
        payroll_year=2025,
        payroll_start=date(2025, 1, 1),
        payroll_frequency="weekly",
    )

    with pytest.raises(IntegrityError):
        PayrollInfo.objects.create(
            payroll_year=2025,
            payroll_start=date(2025, 6, 1),
            payroll_frequency="biweekly",
        )
