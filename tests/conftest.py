import pytest
from pytest_factoryboy import register
from tests.factories import DepartmentFactory, EmployeeFactory

register(DepartmentFactory)
register(EmployeeFactory)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
