# UnDrop Client (Prototype)

A modular Python prototype for a native Unraid "Dropbox-like" sync client that is aware of FUSE filesystems, Unraid shares, and active bidirectional sync.

## Design goals

- Support **bidirectional sync** where local and remote changes can happen concurrently.
- Detect **FUSE-backed roots** and default to conservative sync behavior.
- Detect **Unraid share roots** (`/mnt/user/<share>`) and avoid assumptions about one physical disk.

## Current modules

- `undrop_client.platform.mounts`: parse `/proc/mounts`, resolve root mount.
- `undrop_client.platform.fuse_policy`: derive conservative/safe behavior per mount type.
- `undrop_client.platform.unraid_share`: detect Unraid share context for the sync root.
- `undrop_client.core.scanner`: deterministic local snapshot scanner.
- `undrop_client.sync.models`: cursor/action models for reconciliation.
- `undrop_client.sync.engine`: bidirectional reconciliation and plan generation.
- `undrop_client.providers.base`: provider abstraction for cloud backends.
- `undrop_client.providers.mock_dropbox`: in-memory provider for dev/testing.
- `undrop_client.main`: CLI entrypoint.

## Run

```bash
python -m undrop_client.main --root /path/to/sync/root --dry-run
```

## Test

```bash
pytest
```
