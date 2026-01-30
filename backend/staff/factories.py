import factory
from staff.models import Group, Division, Employee, Location


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
