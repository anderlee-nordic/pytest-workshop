from __future__ import annotations
import pytest

from fixtures.lcs import LifeCycle

type cli_param = str

class TestLifeCycleState:
    @pytest.mark.req_id("REQ-2-1")
    def test_initial_state_is_empty(self, lcs: LifeCycle):
        assert lcs.read_lcs() == "EMPTY"

    @pytest.mark.req_id("REQ-2-2")
    def test_advance_to_opened(self, lcs: LifeCycle):
        lcs.advance_lcs("OPENED")
        assert lcs.read_lcs() == "OPENED"

    def test_full_provisioning_sequence(self, lcs: LifeCycle):
        for state in ["OPENED", "TEST_AND_ASSEMBLY", "DEPLOYED"]:
            lcs.advance_lcs(state)
        assert lcs.read_lcs() == "DEPLOYED"

    # @pytest.mark.parametrize("state", ["OPENED", "TEST_AND_ASSEMBLY"])
    def test_cannot_regress_state(self, lcs: LifeCycle, state: cli_param):
        lcs.advance_lcs("DEPLOYED")
        with pytest.raises(ValueError, match="forward-only"):
            lcs.advance_lcs(state)
