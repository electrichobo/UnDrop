"""Provider abstraction layer."""

from __future__ import annotations

from abc import ABC, abstractmethod

from undrop_client.core.scanner import FileSnapshot


class CloudProvider(ABC):
    """Minimal interface any backend provider should implement."""

    @abstractmethod
    def list_remote(self) -> dict[str, FileSnapshot]:
        """Return remote files indexed by relative path."""

    @abstractmethod
    def upload(self, snapshot: FileSnapshot) -> None:
        """Upload local file metadata/content represented by snapshot."""

    @abstractmethod
    def delete_remote(self, relative_path: str) -> None:
        """Delete a remote file by relative path."""
