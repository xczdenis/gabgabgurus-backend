# pytest_plugins = (
#     "tests.fixtures.test_app",
#     "tests.fixtures.test_client",
#     "tests.fixtures.fake_db",
#     "tests.fixtures.users",
# )
# def pytest_collection_modifyitems(items):
#     for item in items:
#         # if the item belongs to the tests.unit package then add the unit marker
#         if item.module.__name__.startswith("tests.unit"):
#             item.add_marker(pytest.mark.unit)
