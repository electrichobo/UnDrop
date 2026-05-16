"""Mock Dropbox provider for local development and testing."""

from __future__ import annotations

from undrop_client.core.scanner import FileSnapshot
from undrop_client.providers.base import CloudProvider


class MockDropboxProvider(CloudProvider):
    """In-memory provider that behaves like a very small Dropbox subset."""

    def __init__(self) -> None:
        self._remote: dict[str, FileSnapshot] = {}

    def list_remote(self) -> dict[str, FileSnapshot]:
        return dict(self._remote)

    def upload(self, snapshot: FileSnapshot) -> None:
        self._remote[snapshot.relative_path] = snapshot

    def delete_remote(self, relative_path: str) -> None:
        self._remote.pop(relative_path, None)

    def seed_remote(self, snapshot: FileSnapshot) -> None:
        """Test helper for pre-loading remote state."""
        self._remote[snapshot.relative_path] = snapshot
