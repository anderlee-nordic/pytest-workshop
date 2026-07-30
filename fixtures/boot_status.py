import pytest

@pytest.fixture(scope="function")
def read_bootstatus(jlink, console):
    print("  [setup]   read boot status reg")
    yield


@pytest.fixture
def revive_on_failure(request):
    yield
    if request.node.rep_call.failed:
        print(f"\n    [recover]    Test {request.node.name} broke DK. Reviving...")
        fw = getattr(request.node, "fw_ver", None)
        print(f"    [recover logs]    Firmware version at failure: {fw}")
