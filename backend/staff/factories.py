import factory
from staff.models import Group, Division, Employee, Location, Holiday
import pytz
import os
from django.utils import timezone


def current_date():
    today = timezone.now()
    tz_timezone = pytz.timezone(os.environ.get("TIMEZONE"))
    today_tz = today.astimezone(tz_timezone).date()
    return today_tz


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    group_name = factory.Sequence(lambda n: f"Group {n}")


class DivisionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Division

    division_name = factory.Sequence(lambda n: f"Division {n}")


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    location_name = factory.Sequence(lambda n: f"Location {n}")


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    division = factory.SubFactory(DivisionFactory)
    group = factory.SubFactory(GroupFactory)
    location = factory.SubFactory(LocationFactory)


class HolidayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holiday

    holiday_name = factory.Sequence(lambda n: f"Holiday {n}")
    rule_type = "fixed_date"
    observed_rule = "none"
    month = 1
    day = 1
    weekday = 0
    week = 1
