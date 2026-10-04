import json

import pytest

from alphawatch_research.audit import append_audit_record
from alphawatch_research.safety import LiveExecutionDisabled, assert_paper_only


def test_paper_only_guard_rejects_live_or_broker_flags() -> None:
    assert_paper_only(live_enabled=False, broker_enabled=False)
    with pytest.raises(LiveExecutionDisabled):
        assert_paper_only(live_enabled=True, broker_enabled=False)
    with pytest.raises(LiveExecutionDisabled):
        assert_paper_only(live_enabled=False, broker_enabled=True)


def test_audit_record_is_appended_as_jsonl(tmp_path) -> None:
    path = tmp_path / "audit.jsonl"
    append_audit_record(path, action="experiment", message="null result", details={"n": 30})
    row = json.loads(path.read_text(encoding="utf-8").strip())
    assert row["action"] == "experiment"
    assert row["message"] == "null result"
    assert row["details"] == {"n": 30}
