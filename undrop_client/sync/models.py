"""Shared sync models for plan and reconciliation."""

from __future__ import annotations

from dataclasses import dataclass

from undrop_client.core.scanner import FileSnapshot


@dataclass(frozen=True)
class SyncCursorEntry:
    """Last known synced metadata for one relative path."""

    local: FileSnapshot | None
    remote: FileSnapshot | None


@dataclass(frozen=True)
class ReconcileAction:
    """One action chosen by bidirectional reconciliation."""

    relative_path: str
    direction: str
    reason: str
