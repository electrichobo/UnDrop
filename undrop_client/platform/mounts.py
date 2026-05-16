"""Mount inspection helpers for Linux/Unraid hosts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MountInfo:
    """Single mount entry with enough data for sync policy decisions."""

    mount_point: Path
    fs_type: str
    source: str

    @property
    def is_fuse(self) -> bool:
        """True if filesystem type represents a FUSE mount."""
        return self.fs_type.startswith("fuse")


def parse_proc_mounts(proc_mounts_text: str) -> list[MountInfo]:
    """Parse /proc/mounts content into mount records."""
    rows: list[MountInfo] = []
    for line in proc_mounts_text.splitlines():
        if not line.strip():
            continue
        source, mount_point, fs_type, *_ = line.split()
        rows.append(MountInfo(mount_point=Path(mount_point), fs_type=fs_type, source=source))
    return rows


def resolve_mount_for_path(path: Path, mounts: list[MountInfo]) -> MountInfo | None:
    """Return the deepest matching mount point for a given path."""
    path = path.resolve()
    candidates = [m for m in mounts if path == m.mount_point or m.mount_point in path.parents]
    if not candidates:
        return None
    return sorted(candidates, key=lambda m: len(str(m.mount_point)), reverse=True)[0]
