import factory
from planner.models import Holiday


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
