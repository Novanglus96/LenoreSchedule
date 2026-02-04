import factory
from planner.models import Holiday, CalendarEntry
from staff.factories import EmployeeFactory, LocationFactory
from datetime import time


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


class CalendarEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CalendarEntry

    employee = factory.SubFactory(EmployeeFactory)
    calendar_date = factory.Faker("date_object")
    start_time = factory.LazyFunction(lambda: time(9, 0))
    end_time = factory.LazyFunction(lambda: time(17, 0))
    confirmed = False
    location = factory.SubFactory(LocationFactory)
