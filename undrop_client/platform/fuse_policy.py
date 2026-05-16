"""Policy decisions for FUSE and non-FUSE mounts."""

from __future__ import annotations

from dataclasses import dataclass

from undrop_client.platform.mounts import MountInfo


@dataclass(frozen=True)
class SyncSafetyPolicy:
    """Behavior toggles selected from mount capabilities."""

    prefer_polling: bool
    allow_atomic_rename: bool
    note: str


def build_sync_policy(mount: MountInfo | None) -> SyncSafetyPolicy:
    """Build a conservative policy suited for mixed Unraid storage."""
    if mount is None:
        return SyncSafetyPolicy(True, False, "Unknown mount: safest fallback policy applied.")

    if mount.is_fuse:
        # Many FUSE layers have weaker guarantees for eventing and rename atomicity.
        return SyncSafetyPolicy(
            prefer_polling=True,
            allow_atomic_rename=False,
            note=f"FUSE mount detected ({mount.fs_type}); using conservative sync behavior.",
        )

    return SyncSafetyPolicy(
        prefer_polling=False,
        allow_atomic_rename=True,
        note=f"Native filesystem detected ({mount.fs_type}); using standard sync behavior.",
    )
