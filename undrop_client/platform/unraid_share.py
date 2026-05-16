"""Helpers for detecting Unraid user shares and array-aware behavior."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from undrop_client.platform.mounts import MountInfo


@dataclass(frozen=True)
class UnraidShareContext:
    """Captures whether a sync root is an Unraid user share path."""

    is_unraid_share: bool
    share_name: str | None
    note: str


def detect_unraid_share(root: Path, mount: MountInfo | None) -> UnraidShareContext:
    """Detect `/mnt/user/<share>` style roots typically backed by Unraid share FUSE."""
    resolved = root.resolve()
    parts = resolved.parts

    # Unraid user shares are conventionally mounted under /mnt/user/<share-name>.
    if len(parts) >= 4 and parts[:3] == ("/", "mnt", "user"):
        return UnraidShareContext(
            is_unraid_share=True,
            share_name=parts[3],
            note="Unraid user share detected; avoid assumptions about physical disk placement.",
        )

    if mount and mount.fs_type == "fuse.shfs":
        return UnraidShareContext(
            is_unraid_share=True,
            share_name=None,
            note="Unraid share filesystem (fuse.shfs) detected; treating root as share-backed.",
        )

    return UnraidShareContext(False, None, "Path is not an Unraid user share.")
