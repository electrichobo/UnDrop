"""Configuration models for the UnDrop prototype."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SyncConfig:
    """Top-level runtime options for a sync session."""

    root: Path
    dry_run: bool = True
