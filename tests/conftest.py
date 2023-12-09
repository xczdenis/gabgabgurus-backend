import pytest

from tests.utils.helpers import is_integration_test, is_unit_test


def pytest_collection_modifyitems(config, items):
    for item in items:
        if is_unit_test(str(item.fspath)):
            item.add_marker(pytest.mark.unit)
        elif is_integration_test(str(item.fspath)):
            item.add_marker(pytest.mark.integration)


pytest_plugins = (
    "tests.fixtures.users",
    "tests.fixtures.languages",
    "tests.fixtures.countries",
)
