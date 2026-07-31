import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--lcs_state",
        action="append",
        default=[],
        help="list of LCS to pass to test_lcs",
    )


def pytest_generate_tests(metafunc):
    marked = {
        n for m in metafunc.definition.iter_markers("parametrize") \
        for n in m.args[0].split(",")
    }
    if "state" in metafunc.fixturenames and "state" not in marked:
        metafunc.parametrize("state", metafunc.config.getoption("lcs_state"))
