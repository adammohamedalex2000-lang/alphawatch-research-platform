from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class AuditRecord:
    timestamp: str
    action: str
    message: str
    details: dict[str, Any]


def append_audit_record(
    path: str | Path,
    *,
    action: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> AuditRecord:
    """Append one transparent JSONL audit record."""

    record = AuditRecord(
        timestamp=datetime.now(UTC).isoformat(),
        action=action,
        message=message,
        details=details or {},
    )
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")
    return record
