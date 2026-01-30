import factory
from staff.models import Group, Division, Employee


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    group_name = factory.Sequence(lambda n: f"Group {n}")


class DivisionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Division

    division_name = factory.Sequence(lambda n: f"Division {n}")


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    division = factory.SubFactory(DivisionFactory)
    group = factory.SubFactory(GroupFactory)
