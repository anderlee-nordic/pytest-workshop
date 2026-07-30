import pytest


# Mock LCS. NOT REAL!
LCS_ORDER = ["EMPTY", "OPENED", "TEST_AND_ASSEMBLY", "DEPLOYED", "DECOMMISSIONED"]


class LifeCycle:
    """Forward-only life cycle state model for the target [SIM]."""
    def __init__(self, jlink):
        self._jlink = jlink
        self.state = "EMPTY"

    def read_lcs(self):
        return self.state

    def advance_lcs(self, target):
        if target not in LCS_ORDER:
            raise ValueError(f"unknown LCS: {target}")
        if LCS_ORDER.index(target) <= LCS_ORDER.index(self.state):
            raise ValueError(f"LCS is forward-only: cannot go {self.state} -> {target}")
        self.state = target


@pytest.fixture
def lcs(jlink):
    lifecycle = LifeCycle(jlink)
    print("\n  [setup]   LCS reset to EMPTY")
    yield lifecycle
    print(f"\n  [teardown] LCS left at {lifecycle.read_lcs()}")
