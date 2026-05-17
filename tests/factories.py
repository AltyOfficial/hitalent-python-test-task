import factory
from factory.django import DjangoModelFactory
from server.apps.departments.models import Department, Employee
from django.utils import timezone


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.Sequence(lambda n: f"Department {n}")


class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    full_name = factory.Faker("name")
    position = factory.Iterator(["Developer", "Manager", "Designer", "Analyst"])
    department = factory.SubFactory(DepartmentFactory)
    hired_at = factory.LazyFunction(timezone.now)
