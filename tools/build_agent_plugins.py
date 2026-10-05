"""Build portable Agent Plugins 1.0 packages from canonical skill sources.

Usage:
    python tools/build_agent_plugins.py --check                 # validate profiles/composition only
    python tools/build_agent_plugins.py --out dist/agent-plugins  # build stable packages
    python tools/build_agent_plugins.py --out dist/agent-plugins --zip --include-preview

Inputs: catalog/skills.json, packaging/agent-plugins/profiles.yaml, package.json.
Every packaged SKILL.md (and its sibling files) is a byte-identical copy of the
canonical directory; AGILE_V_PACKAGE_MANIFEST.json records source path, commit
and digest per skill. Integrity/provenance of a package says nothing about the
correctness of the skills it contains.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from jsonschema import Draft202012Validator

try:
    from tools._common import ROOT, dump_json, load_json, load_yaml, package_version, sha256_bytes
except ImportError:  # executed as a script: tools/ is sys.path[0]
    from _common import ROOT, dump_json, load_json, load_yaml, package_version, sha256_bytes  # noqa: E402

PACKAGING = ROOT / "packaging" / "agent-plugins"
PLUGIN_SCHEMA = PACKAGING / "schemas" / "1.0.0" / "plugin.schema.json"
PLUGIN_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
EXTENSION_NS = "org.agile-v"
SOURCE_REPOSITORY = "Agile-V/agile_v_skills"
EXCLUDED_PARTS = {"__pycache__", ".DS_Store", "node_modules"}
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)


class CompositionError(ValueError):
    pass


# --- profiles and composition ----------------------------------------------

def load_profiles() -> dict[str, dict]:
    data = load_yaml(PACKAGING / "profiles.yaml")
    errors = list(Draft202012Validator(load_json(PACKAGING / "profile.schema.json")).iter_errors(data))
    if errors:
        raise CompositionError([e.message for e in errors])
    profiles = {}
    for profile in data["profiles"]:
        if profile["name"] in profiles:
            raise CompositionError(f"duplicate profile {profile['name']}")
        profiles[profile["name"]] = dict(profile)
    for profile in profiles.values():
        if "extends" in profile:
            base = profiles.get(profile["extends"])
            if base is None or "extends" in base:
                raise CompositionError(f"{profile['name']}: invalid extends")
            profile["include"] = list(dict.fromkeys(base["include"] + profile["include"]))
    return profiles


def catalog_skills(catalog: dict | None = None) -> dict[str, dict]:
    catalog = catalog or load_json(ROOT / "catalog" / "skills.json")
    return {entry["name"]: entry for entry in catalog["skills"]}


def check_composition(profile: dict, skills: dict[str, dict]) -> list[str]:
    """Return composition errors (empty list = composable).

    Rejects: unknown skill, unsatisfied prerequisite, missing required
    capability, duplicate exclusive capability, direct conflict, stable
    profile containing or depending on a draft-only capability, and
    including a skill together with a skill that supersedes its capability.
    """
    errors: list[str] = []
    name, stable = profile["name"], profile["channel"] == "stable"
    included = profile["include"]
    unknown = [s for s in included if s not in skills]
    if unknown:
        return [f"{name}: unknown skill(s) {unknown}"]
    members = [skills[s] for s in included]
    for entry in members:
        if stable and entry["status"] == "draft":
            errors.append(f"{name}: stable profile contains draft skill {entry['name']}")
        missing = set(entry["routing"]["prerequisites"]) - set(included)
        if missing:
            errors.append(f"{name}: {entry['name']} prerequisite(s) not included: {sorted(missing)}")
    provided: dict[str, list[str]] = {}
    for entry in members:
        for capability in entry.get("capabilities", {}).get("provides", []):
            provided.setdefault(capability, []).append(entry["name"])
    released_provided = {c for c, owners in provided.items()
                         if any(skills[o]["status"] == "released" for o in owners)}
    for entry in members:
        caps = entry.get("capabilities")
        if caps is None:
            errors.append(f"{name}: {entry['name']} has no capability metadata")
            continue
        for capability in caps["requires"]:
            if capability not in provided:
                errors.append(f"{name}: {entry['name']} requires missing capability {capability}")
            elif stable and capability not in released_provided:
                errors.append(f"{name}: {entry['name']} depends on draft-only capability {capability}")
        for capability in caps["conflicts"]:
            if capability in provided:
                errors.append(f"{name}: {entry['name']} conflicts with {capability} ({provided[capability]})")
        for capability in caps.get("exclusive", []):
            if len(provided.get(capability, [])) > 1:
                errors.append(f"{name}: exclusive capability {capability} provided by {provided[capability]}")
        for capability in caps["supersedes"]:
            if capability in provided:
                errors.append(f"{name}: {entry['name']} supersedes {capability} also provided by {provided[capability]}")
    return errors


# --- Agent Skills conformance (subset checked at package time) --------------

def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise CompositionError(f"{path}: missing frontmatter")
    return load_yaml_text(text.split("---", 2)[1])


def load_yaml_text(text: str) -> dict:
    import yaml
    return yaml.safe_load(text) or {}


def check_agent_skill(skill_dir: Path) -> list[str]:
    import re
    meta = _frontmatter(skill_dir / "SKILL.md")
    errors = []
    name, description = meta.get("name"), meta.get("description")
    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name {name!r} must equal directory name")
    if not isinstance(name, str) or not re.fullmatch(r"(?!.*--)[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", name):
        errors.append(f"{skill_dir.name}: invalid Agent Skills name")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        errors.append(f"{skill_dir.name}: description must be 1-1024 characters")
    return errors


# --- package building --------------------------------------------------------

def git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                              check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def git_tree_clean() -> bool | None:
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout
        return out.strip() == ""
    except (OSError, subprocess.CalledProcessError):
        return None


def _skill_files(skill_dir: Path) -> list[Path]:
    files = []
    for path in sorted(skill_dir.rglob("*")):
        rel = path.relative_to(skill_dir)
        if any(part in EXCLUDED_PARTS or part.startswith(".") for part in rel.parts):
            continue
        if path.is_symlink():
            raise CompositionError(f"{path.relative_to(ROOT)}: symlinks are not packaged")
        if path.is_file():
            files.append(path)
    return files


def _digest_files(base: Path, files: list[Path]) -> str:
    lines = sorted(f"{f.relative_to(base).as_posix()}\0{hashlib.sha256(f.read_bytes()).hexdigest()}\n" for f in files)
    return sha256_bytes("".join(lines).encode())


def plugin_manifest(profile: dict, version: str) -> dict:
    manifest = {
        "$schema": PLUGIN_SCHEMA_ID,
        "name": profile["name"],
        "version": version,
        "description": profile["description"],
        "author": {"name": "Agile V", "url": "https://agile-v.org"},
        "homepage": "https://agile-v.org",
        "repository": "https://github.com/Agile-V/agile_v_skills",
        "license": "CC-BY-SA-4.0",
        "keywords": ["agile-v", "agent-skills", "traceability", "verification"],
        "extensions": {EXTENSION_NS: {"channel": profile["channel"],
                                      "package_manifest": "./AGILE_V_PACKAGE_MANIFEST.json"}},
    }
    errors = list(Draft202012Validator(load_json(PLUGIN_SCHEMA)).iter_errors(manifest))
    if errors:
        raise CompositionError([e.message for e in errors])
    return manifest


def build_package(profile: dict, out_dir: Path, *, skills: dict[str, dict], version: str,
                  commit: str, tree_clean: bool | None) -> Path:
    errors = check_composition(profile, skills)
    if errors:
        raise CompositionError(errors)
    root = out_dir / f"{profile['name']}-{version}"
    if root.exists():
        shutil.rmtree(root)
    (root / "skills").mkdir(parents=True)
    records = []
    for name in sorted(profile["include"]):
        entry = skills[name]
        source_dir = ROOT / Path(entry["path"]).parent
        errors = check_agent_skill(source_dir)
        if errors:
            raise CompositionError(errors)
        target_dir = root / "skills" / name
        files = _skill_files(source_dir)
        for path in files:
            target = target_dir / path.relative_to(source_dir)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
            if not target.resolve().is_relative_to(root.resolve()):
                raise CompositionError(f"{target}: escapes plugin root")
        records.append({
            "skill": name,
            "source_repository": SOURCE_REPOSITORY,
            "source_commit": commit,
            "source_path": Path(entry["path"]).parent.as_posix() + "/",
            "skill_version": entry["version"],
            "skill_status": entry["status"],
            "skill_md_digest": sha256_bytes((source_dir / "SKILL.md").read_bytes()),
            "content_digest": _digest_files(source_dir, files),
        })
    shutil.copyfile(ROOT / "LICENSE", root / "LICENSE")
    shutil.copyfile(ROOT / "CHANGELOG.md", root / "CHANGELOG.md")
    (root / "plugin.json").write_text(dump_json(plugin_manifest(profile, version)), encoding="utf-8")
    payload = [p for p in sorted(root.rglob("*")) if p.is_file()]
    manifest = {
        "schema_version": "1.0",
        "package": profile["name"],
        "package_version": version,
        "channel": profile["channel"],
        "agent_plugins_spec": "1.0.0",
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": commit,
        "source_tree_clean": tree_clean,
        "contract_versions_ref": "contracts/versions.yaml",
        "skills": records,
        "payload_digest": _digest_files(root, payload),
        "provenance_note": ("Digests bind package bytes to canonical sources. They do not establish that "
                            "the skills are correct, enforced by any runtime, or fit for a purpose."),
    }
    (root / "AGILE_V_PACKAGE_MANIFEST.json").write_text(dump_json(manifest), encoding="utf-8")
    return root


def deterministic_zip(package_dir: Path, zip_path: Path) -> str:
    files = sorted(p for p in package_dir.rglob("*") if p.is_file())
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo(f"{package_dir.name}/{path.relative_to(package_dir).as_posix()}", ZIP_EPOCH)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    return hashlib.sha256(zip_path.read_bytes()).hexdigest()


def build_all(out_dir: Path, *, include_preview: bool = False, make_zip: bool = False,
              commit: str | None = None) -> list[dict]:
    profiles = load_profiles()
    skills = catalog_skills()
    version = package_version()
    commit = commit or git_commit()
    clean = git_tree_clean()
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for profile in profiles.values():
        if profile["channel"] != "stable" and not include_preview:
            continue
        package = build_package(profile, out_dir, skills=skills, version=version, commit=commit, tree_clean=clean)
        result = {"name": profile["name"], "channel": profile["channel"], "path": package}
        if make_zip:
            zip_path = out_dir / f"{package.name}.zip"
            result["zip"] = zip_path
            result["sha256"] = deterministic_zip(package, zip_path)
        results.append(result)
    if make_zip:
        lines = "".join(f"{r['sha256']}  {r['zip'].name}\n" for r in sorted(results, key=lambda r: r["zip"].name))
        (out_dir / "SHA256SUMS").write_text(lines, encoding="utf-8")
    return results


def check_all() -> list[str]:
    errors = []
    profiles = load_profiles()
    skills = catalog_skills()
    for profile in profiles.values():
        errors += check_composition(profile, skills)
        for name in profile["include"]:
            if name in skills:
                errors += check_agent_skill(ROOT / Path(skills[name]["path"]).parent)
    plugin_manifest(next(iter(profiles.values())), package_version())
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="validate profiles and composition only")
    parser.add_argument("--out", type=Path, default=ROOT / "dist" / "agent-plugins")
    parser.add_argument("--zip", action="store_true", help="also write deterministic ZIPs and SHA256SUMS")
    parser.add_argument("--include-preview", action="store_true", help="also build preview-channel profiles")
    parser.add_argument("--commit", help="source commit to record (default: git HEAD)")
    args = parser.parse_args(argv)
    try:
        if args.check:
            errors = check_all()
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1 if errors else 0
        for result in build_all(args.out, include_preview=args.include_preview, make_zip=args.zip,
                                commit=args.commit):
            print(json.dumps({k: str(v) for k, v in result.items()}))
    except CompositionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    os.umask(0o022)
    sys.exit(main())
