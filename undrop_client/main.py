"""CLI entrypoint for UnDrop prototype."""

from __future__ import annotations

import argparse
from pathlib import Path

from undrop_client.providers.mock_dropbox import MockDropboxProvider
from undrop_client.sync.engine import build_plan, execute_plan


def read_proc_mounts() -> str:
    """Read Linux mount table used for filesystem capability detection."""
    return Path("/proc/mounts").read_text(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UnDrop: Unraid-native Dropbox-style sync prototype")
    parser.add_argument("--root", type=Path, required=True, help="Sync root folder")
    parser.add_argument("--dry-run", action="store_true", help="Print what would upload without mutating remote")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    provider = MockDropboxProvider()
    plan = build_plan(root=args.root, provider=provider, proc_mounts_text=read_proc_mounts())

    print(f"Policy: {plan.policy.note}")
    print(f"Share context: {plan.share_context.note}")
    print(f"Planned actions: {len(plan.actions)}")

    applied = execute_plan(plan=plan, provider=provider, dry_run=args.dry_run)
    print(f"Actions {'planned' if args.dry_run else 'applied'}: {applied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
