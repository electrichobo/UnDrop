from pathlib import Path

from undrop_client.core.scanner import FileSnapshot
from undrop_client.providers.mock_dropbox import MockDropboxProvider
from undrop_client.sync.engine import build_plan, reconcile_bidirectional
from undrop_client.sync.models import SyncCursorEntry


def test_bidirectional_prefers_download_when_remote_only_changed() -> None:
    path = "a.txt"
    remote_snap = FileSnapshot(relative_path=path, size=3, mtime_ns=2)
    cursor = {path: SyncCursorEntry(local=None, remote=None)}
    actions = reconcile_bidirectional(local={}, remote={path: remote_snap}, cursor=cursor)
    assert len(actions) == 1
    assert actions[0].direction == "download"


def test_build_plan_detects_unraid_share_context(tmp_path: Path) -> None:
    # Build a nested path that matches /mnt/user/<share> convention.
    root = Path("/mnt/user/media")
    provider = MockDropboxProvider()
    mounts = "shfs /mnt/user fuse.shfs rw 0 0\n"
    plan = build_plan(root, provider, mounts)
    assert plan.share_context.is_unraid_share is True


def test_build_plan_detects_upload_from_local_file(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    provider = MockDropboxProvider()
    plan = build_plan(tmp_path, provider, "/dev/sda1 / ext4 rw 0 0\n")
    assert any(action.direction == "upload" for action in plan.actions)
