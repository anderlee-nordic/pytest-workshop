import pytest
from pytest_html import extras


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call":
        fw = getattr(item, "fw_ver", None)
        if fw:
            report.sections.append(("Firmware version", fw))

        req_ids = [m.args[0] for m in item.iter_markers(name="req_id")]
        report.req_id = ", ".join(req_ids)


def pytest_html_results_table_header(cells):
    cells.append("<th>Requirement ID</th>")

def pytest_html_results_table_row(report, cells):
    cells.append(f"<td>{getattr(report, 'req_id', '')}</td>")

def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="req_id"):
            req_id = marker.args[0]
            item.user_properties.append(("Requirement ID", req_id))
