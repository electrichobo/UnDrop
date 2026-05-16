from pathlib import Path

from undrop_client.platform.fuse_policy import build_sync_policy
from undrop_client.platform.mounts import MountInfo, parse_proc_mounts, resolve_mount_for_path


def test_parse_and_resolve_mount() -> None:
    mounts = parse_proc_mounts("/dev/sda1 / ext4 rw 0 0\nrclone /mnt/remote fuse.rclone rw 0 0\n")
    match = resolve_mount_for_path(Path("/mnt/remote/media"), mounts)
    assert match is not None
    assert match.fs_type == "fuse.rclone"


def test_fuse_mount_gets_conservative_policy() -> None:
    mount = MountInfo(mount_point=Path("/mnt/remote"), fs_type="fuse.rclone", source="rclone")
    policy = build_sync_policy(mount)
    assert policy.prefer_polling is True
    assert policy.allow_atomic_rename is False
