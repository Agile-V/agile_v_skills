"""Shared helpers for deterministic generators.

Every generator supports ``--check``: regenerate in memory and fail (exit 1)
if the committed output differs. CI uses ``--check`` so drift fails the PR.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data) -> str:
    """Stable on-disk JSON: sorted keys, 2-space indent, trailing newline."""
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n"


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def tree_digest(paths: list[Path], root: Path = ROOT) -> str:
    """Digest of a file set: sha256 over sorted 'relpath\\0sha256hex\\n' lines.

    Path order and filesystem metadata never influence the result.
    """
    lines = sorted(f"{p.relative_to(root).as_posix()}\0{hashlib.sha256(p.read_bytes()).hexdigest()}\n"
                   for p in paths)
    return sha256_bytes("".join(lines).encode("utf-8"))


def write_or_check(path: Path, content: str, check: bool) -> bool:
    """Write content, or in check mode report whether it already matches."""
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            print(f"DRIFT: {path.relative_to(ROOT)} is not up to date; regenerate it.", file=sys.stderr)
            return False
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def package_version() -> str:
    return load_json(ROOT / "package.json")["version"]
