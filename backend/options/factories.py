import factory
from datetime import date
from options.models import PayrollInfo


class PayrollInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PayrollInfo

    payroll_year = factory.Sequence(lambda n: 2020 + n)
    payroll_start = factory.LazyAttribute(lambda o: date(o.payroll_year, 1, 1))
    payroll_frequency = "weekly"
    first_day = None
    second_day = None
