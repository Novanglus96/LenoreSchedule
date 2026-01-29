import factory
from staff.models import Group, Department, Employee


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    group_name = factory.Sequence(lambda n: f"Group {n}")


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    department_name = factory.Sequence(lambda n: f"Department {n}")


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    department = factory.SubFactory(DepartmentFactory)
    group = factory.SubFactory(GroupFactory)
