from tests.settings import test_settings


def add_test_prefix(input_string: str) -> str:
    return f"{test_settings.PREFIX_FOR_FAKE_OBJECTS}-{input_string}"


def is_unit_test(filepath):
    return test_settings.UNIT_TESTS_DIR in str(filepath)


def is_integration_test(filepath):
    return test_settings.INTEGRATION_TESTS_DIR in str(filepath)
