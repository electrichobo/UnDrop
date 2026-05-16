"""Filesystem scanning primitives for sync planning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileSnapshot:
    """Small metadata object for deciding whether to sync a file."""

    relative_path: str
    size: int
    mtime_ns: int


def scan_tree(root: Path) -> list[FileSnapshot]:
    """Return deterministic file metadata snapshots beneath root."""
    snapshots: list[FileSnapshot] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        stat = path.stat()
        snapshots.append(
            FileSnapshot(
                relative_path=str(path.relative_to(root)),
                size=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
            )
        )
    return snapshots
