"""Protected supplied-file integrity checks shared by ASE Semester 7 labs."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath


class IntegrityError(ValueError):
    """A supplied lab file differs from the released package."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_inventory(lab_root: Path, expected_inventory_sha256: str) -> dict[str, str]:
    """Verify the protected inventory and every immutable supplied file it names."""
    data_root = (lab_root / "data").resolve()
    inventory_path = data_root / "checksums.sha256"
    if not inventory_path.is_file():
        raise IntegrityError("data/checksums.sha256 is missing; restore the released lab copy")
    if sha256(inventory_path) != expected_inventory_sha256:
        raise IntegrityError("data/checksums.sha256 differs from the released inventory")
    observed: dict[str, str] = {}
    inventory_lines = inventory_path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(inventory_lines, start=1):
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or re.fullmatch(r"[0-9a-f]{64}", parts[0]) is None:
            raise IntegrityError(f"invalid checksum inventory entry on line {line_number}")
        relative = parts[1].strip().replace("\\", "/")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or not pure.parts or relative in observed:
            raise IntegrityError("data/checksums.sha256 contains an unsafe or duplicate path")
        target = data_root.joinpath(*pure.parts)
        try:
            target.resolve().relative_to(data_root)
        except ValueError as error:
            raise IntegrityError("checksum inventory path leaves data/") from error
        if not target.is_file() or sha256(target) != parts[0]:
            raise IntegrityError(f"supplied file data/{relative} is missing or changed")
        observed[relative] = parts[0]
    if not observed:
        raise IntegrityError("data/checksums.sha256 is empty")
    return observed
