import factory
from staff.models import Group, Department


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    group_name = factory.Sequence(lambda n: f"Group {n}")


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    department_name = factory.Sequence(lambda n: f"Department {n}")
