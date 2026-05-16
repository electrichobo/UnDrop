"""Sync engine orchestration for local-to-cloud propagation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from undrop_client.core.scanner import FileSnapshot, scan_tree
from undrop_client.platform.fuse_policy import SyncSafetyPolicy, build_sync_policy
from undrop_client.platform.mounts import MountInfo, parse_proc_mounts, resolve_mount_for_path
from undrop_client.platform.unraid_share import UnraidShareContext, detect_unraid_share
from undrop_client.providers.base import CloudProvider
from undrop_client.sync.models import ReconcileAction, SyncCursorEntry


@dataclass(frozen=True)
class SyncPlan:
    """Computed sync action summary."""

    policy: SyncSafetyPolicy
    share_context: UnraidShareContext
    actions: list[ReconcileAction]


def reconcile_bidirectional(
    local: dict[str, FileSnapshot],
    remote: dict[str, FileSnapshot],
    cursor: dict[str, SyncCursorEntry],
) -> list[ReconcileAction]:
    """Create actions for active bidirectional sync using last-synced cursor state."""
    actions: list[ReconcileAction] = []

    for rel in sorted(set(local) | set(remote) | set(cursor)):
        cur = cursor.get(rel)
        local_now = local.get(rel)
        remote_now = remote.get(rel)
        local_prev = cur.local if cur else None
        remote_prev = cur.remote if cur else None

        local_changed = local_now != local_prev
        remote_changed = remote_now != remote_prev

        if local_now is None and remote_now is None:
            continue
        if local_changed and not remote_changed and local_now is not None:
            actions.append(ReconcileAction(rel, "upload", "local changed while remote unchanged"))
        elif remote_changed and not local_changed and remote_now is not None:
            actions.append(ReconcileAction(rel, "download", "remote changed while local unchanged"))
        elif local_changed and remote_changed:
            actions.append(ReconcileAction(rel, "conflict", "both sides changed since last sync"))
        elif cur is None:
            # Bootstrap path for first sync when both sides differ.
            direction = "upload" if local_now and not remote_now else "download"
            actions.append(ReconcileAction(rel, direction, "first sync bootstrap"))

    return actions


def build_plan(
    root: Path,
    provider: CloudProvider,
    proc_mounts_text: str,
    cursor: dict[str, SyncCursorEntry] | None = None,
) -> SyncPlan:
    """Build a sync plan for active bidirectional array/share environments."""
    mounts: list[MountInfo] = parse_proc_mounts(proc_mounts_text)
    mount = resolve_mount_for_path(root, mounts)
    policy = build_sync_policy(mount)
    share_context = detect_unraid_share(root, mount)

    local = {s.relative_path: s for s in scan_tree(root)}
    remote = provider.list_remote()
    actions = reconcile_bidirectional(local, remote, cursor or {})

    return SyncPlan(policy=policy, share_context=share_context, actions=actions)


def execute_plan(plan: SyncPlan, provider: CloudProvider, dry_run: bool) -> int:
    """Apply plan and return count of non-conflict actions."""
    actionable = [a for a in plan.actions if a.direction in {"upload", "delete_remote"}]
    if dry_run:
        return len(actionable)

    for action in actionable:
        if action.direction == "upload":
            # Caller computes payload externally; this prototype only shows action accounting.
            continue
        if action.direction == "delete_remote":
            provider.delete_remote(action.relative_path)
    return len(actionable)
