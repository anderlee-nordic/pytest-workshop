import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--lcs_state",
        action="append",
        default=[],
        help="list of LCS to pass to test_lcs",
    )


def pytest_generate_tests(metafunc):
    if "state" in metafunc.fixturenames:
        metafunc.parametrize("state", metafunc.config.getoption("lcs_state"))
