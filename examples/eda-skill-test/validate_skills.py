#!/usr/bin/env python3
"""
EDA Skill Pipeline Validator

Validates all 26 EDA domain SKILL.md files for:
1. YAML frontmatter schema correctness
2. Required markdown sections
3. Prerequisite DAG integrity (no cycles, all references resolve)
4. Sequential skill numbering
5. Group assignment consistency
6. V-Model position correctness

Usage:
    python validate_skills.py [--skills-dir PATH]

Default skills dir: ../../domains/eda/
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    # Fallback: minimal YAML parser for frontmatter
    yaml = None


# ─── Constants ───────────────────────────────────────────────────────────────

EXPECTED_SKILL_COUNT = 26

REQUIRED_FRONTMATTER_FIELDS = {
    "name": str,
    "description": str,
    "license": str,
}

REQUIRED_METADATA_FIELDS = {
    "version": str,
    "standard": str,
    "domain": str,
    "group": str,
    "position": str,
    "skill_number": int,
    "prerequisite": str,
    "author": str,
}

VALID_GROUPS = {"A", "B", "C", "D", "E", "F"}

VALID_POSITIONS = {"left", "apex", "right"}

# Expected V-model position by group
GROUP_POSITION_MAP = {
    "A": "left",
    "B": "left",
    "C": "apex",  # library-qa (#13) is "right" — exception
    "D": "apex",
    "E": "right",
    "F": "right",
}

# Known exceptions to group→position mapping
POSITION_EXCEPTIONS = {
    "eda-library-qa": ("C", "right"),  # QA/verification role despite being in Group C
}

REQUIRED_SECTIONS = [
    r"##\s+(?:Instructions?|Context\s+Engineering|Tool\s+Recommendations?|[\w\s]+Strategy)",
    r"##\s+Inputs?",
    r"##\s+Outputs?(?:\s+Schema)?",
    r"##\s+Guardrails?",
    r"##\s+Halt\s+Conditions?",
]

ALL_SKILL_DIRS = [
    "requirements-normalizer",
    "schematic-sheet-plan",
    "power-tree-plan",
    "power-path-selector",
    "controller-selector",
    "interface-selector",
    "protection-emc-selector",
    "analog-frontend-selector",
    "bom-risk-check",
    "symbol-builder",
    "footprint-builder",
    "symbol-footprint-mapper",
    "library-qa",
    "template-instantiator",
    "placement-engine",
    "connectivity-synthesizer",
    "support-passives",
    "net-naming-hygiene",
    "file-integrity-check",
    "kicad-render-test",
    "kicad-erc-gate",
    "protocol-rule-checks",
    "library-resolution-check",
    "bom-generator",
    "documentation-packager",
    "layout-handoff-exporter",
]


# ─── Helpers ─────────────────────────────────────────────────────────────────


def parse_frontmatter(content: str) -> tuple[dict[str, Any] | None, str]:
    """Extract YAML frontmatter and body from a SKILL.md file."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return None, content

    raw_yaml = match.group(1)
    body = match.group(2)

    if yaml:
        data = yaml.safe_load(raw_yaml)
    else:
        # Minimal parser: handles flat keys and one level of nesting
        data = {}
        current_section = None
        for line in raw_yaml.split("\n"):
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            # Top-level key
            top_match = re.match(r"^(\w[\w-]*)\s*:\s*(.*)$", line)
            if top_match:
                key = top_match.group(1)
                val = top_match.group(2).strip().strip('"').strip("'")
                if val:
                    data[key] = val
                    current_section = None
                else:
                    data[key] = {}
                    current_section = key
                continue
            # Nested key
            nested_match = re.match(r"^\s+(\w[\w-]*)\s*:\s*(.*)$", line)
            if nested_match and current_section:
                key = nested_match.group(1)
                val = nested_match.group(2).strip().strip('"').strip("'")
                data[current_section][key] = val

    return data, body


def check_dag_cycles(adjacency: dict[str, list[str]]) -> list[list[str]]:
    """Detect cycles in the prerequisite DAG using DFS."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    cycles = []

    def dfs(node: str, path: list[str]):
        color[node] = GRAY
        path.append(node)
        for neighbor in adjacency.get(node, []):
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)
        path.pop()
        color[node] = BLACK

    for node in adjacency:
        if color[node] == WHITE:
            dfs(node, [])

    return cycles


def topological_sort(adjacency: dict[str, list[str]], all_nodes: set[str]) -> list[str]:
    """Return topologically sorted list of skills (prerequisites first)."""
    in_degree = defaultdict(int)
    for node in all_nodes:
        in_degree[node] = 0
    for node, deps in adjacency.items():
        for dep in deps:
            in_degree[node] += 1  # node depends on dep

    queue = [n for n in all_nodes if in_degree[n] == 0]
    queue.sort()
    result = []

    reverse_adj = defaultdict(list)
    for node, deps in adjacency.items():
        for dep in deps:
            reverse_adj[dep].append(node)

    # Kahn's algorithm
    in_deg = defaultdict(int)
    for node, deps in adjacency.items():
        in_deg[node] = len(deps)
    for node in all_nodes:
        if node not in in_deg:
            in_deg[node] = 0

    queue = sorted([n for n in all_nodes if in_deg[n] == 0])
    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)
        for dependent in sorted(reverse_adj.get(node, [])):
            in_deg[dependent] -= 1
            if in_deg[dependent] == 0:
                queue.append(dependent)

    return result


# ─── Validator ───────────────────────────────────────────────────────────────


class SkillValidator:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.skills: dict[str, dict] = {}  # name -> frontmatter
        self.adjacency: dict[str, list[str]] = {}  # name -> [prerequisites]

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def validate_all(self) -> bool:
        """Run all validations. Returns True if all pass."""
        print("=" * 70)
        print("EDA Skill Pipeline Validator")
        print("=" * 70)
        print(f"Skills directory: {self.skills_dir}")
        print()

        # Phase 1: Check all expected directories exist
        self._check_directories()

        # Phase 2: Parse and validate each SKILL.md
        self._validate_individual_skills()

        # Phase 3: Validate DAG integrity
        self._validate_dag()

        # Phase 4: Validate sequencing
        self._validate_sequencing()

        # Phase 5: Summary
        self._print_summary()

        return len(self.errors) == 0

    def _check_directories(self):
        print("[1/4] Checking directory structure...")
        found = []
        missing = []
        for dirname in ALL_SKILL_DIRS:
            skill_path = self.skills_dir / dirname / "SKILL.md"
            if skill_path.exists():
                found.append(dirname)
            else:
                missing.append(dirname)
                self.error(f"Missing SKILL.md: {dirname}/SKILL.md")

        print(f"  Found: {len(found)}/{EXPECTED_SKILL_COUNT} skill directories")
        if missing:
            print(f"  Missing: {', '.join(missing)}")
        else:
            print("  All directories present.")

        # Check supplementary files
        domain_md = self.skills_dir / "DOMAIN.md"
        if not domain_md.exists():
            self.error("Missing DOMAIN.md")
        else:
            print("  DOMAIN.md: present")

        docs_dir = self.skills_dir / "docs"
        expected_docs = [
            "pcb_guidelines.md",
            "validation_checklist.md",
            "kicad_api_reference.md",
        ]
        for doc in expected_docs:
            if (docs_dir / doc).exists():
                print(f"  docs/{doc}: present")
            else:
                self.warn(f"Missing optional doc: docs/{doc}")

        print()

    def _validate_individual_skills(self):
        print("[2/4] Validating individual SKILL.md files...")
        skill_numbers_seen = {}

        for dirname in ALL_SKILL_DIRS:
            skill_path = self.skills_dir / dirname / "SKILL.md"
            if not skill_path.exists():
                continue

            content = skill_path.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(content)

            if frontmatter is None:
                self.error(f"{dirname}: No YAML frontmatter found")
                continue

            # Check required top-level fields
            for field, expected_type in REQUIRED_FRONTMATTER_FIELDS.items():
                if field not in frontmatter:
                    self.error(f"{dirname}: Missing frontmatter field '{field}'")
                elif not isinstance(frontmatter[field], expected_type):
                    self.error(
                        f"{dirname}: Field '{field}' should be {expected_type.__name__}, "
                        f"got {type(frontmatter[field]).__name__}"
                    )

            # Check metadata block
            metadata = frontmatter.get("metadata", {})
            if not metadata:
                self.error(f"{dirname}: Missing 'metadata' block")
                continue

            for field, expected_type in REQUIRED_METADATA_FIELDS.items():
                if field not in metadata:
                    self.error(f"{dirname}: Missing metadata field '{field}'")
                else:
                    val = metadata[field]
                    # skill_number may be parsed as string by minimal parser
                    if field == "skill_number":
                        try:
                            val = int(val)
                        except (ValueError, TypeError):
                            self.error(
                                f"{dirname}: metadata.skill_number is not an integer: {val}"
                            )
                            continue

            # Validate specific field values
            name = frontmatter.get("name", "")
            if not name.startswith("eda-"):
                self.error(f"{dirname}: name should start with 'eda-', got '{name}'")

            license_val = frontmatter.get("license", "")
            if license_val != "CC-BY-SA-4.0":
                self.warn(f"{dirname}: Unexpected license '{license_val}'")

            group = metadata.get("group", "")
            if group not in VALID_GROUPS:
                self.error(
                    f"{dirname}: Invalid group '{group}', expected one of {VALID_GROUPS}"
                )

            position = metadata.get("position", "")
            if position not in VALID_POSITIONS:
                self.error(
                    f"{dirname}: Invalid position '{position}', expected one of {VALID_POSITIONS}"
                )

            # Check group→position consistency
            if name in POSITION_EXCEPTIONS:
                expected_group, expected_pos = POSITION_EXCEPTIONS[name]
                if group != expected_group or position != expected_pos:
                    self.warn(
                        f"{dirname}: Expected exception ({expected_group}, {expected_pos}), "
                        f"got ({group}, {position})"
                    )
            elif group in GROUP_POSITION_MAP and position != GROUP_POSITION_MAP[group]:
                self.error(
                    f"{dirname}: Group '{group}' should have position "
                    f"'{GROUP_POSITION_MAP[group]}', got '{position}'"
                )

            # Skill number uniqueness
            skill_num = 0
            try:
                skill_num = int(metadata.get("skill_number", 0))
                if skill_num in skill_numbers_seen:
                    self.error(
                        f"{dirname}: Duplicate skill_number {skill_num} "
                        f"(also in {skill_numbers_seen[skill_num]})"
                    )
                skill_numbers_seen[skill_num] = dirname
            except (ValueError, TypeError):
                pass

            # Check required markdown sections
            for pattern in REQUIRED_SECTIONS:
                if not re.search(pattern, body, re.IGNORECASE):
                    section_name = pattern.replace(r"\s+", " ").replace(r"##\s+", "## ")
                    self.warn(
                        f"{dirname}: Missing expected section matching '{section_name}'"
                    )

            # Store for DAG analysis
            prereqs_raw = metadata.get("prerequisite", "")
            prereqs = [p.strip() for p in prereqs_raw.split(",") if p.strip()]
            self.skills[name] = frontmatter
            self.adjacency[name] = prereqs

            print(f"  [{skill_num:2d}] {name} (Group {group}, {position}) — OK")

        # Check sequential numbering
        expected_numbers = set(range(1, EXPECTED_SKILL_COUNT + 1))
        actual_numbers = set(skill_numbers_seen.keys())
        missing_numbers = expected_numbers - actual_numbers
        extra_numbers = actual_numbers - expected_numbers

        if missing_numbers:
            self.error(f"Missing skill_numbers: {sorted(missing_numbers)}")
        if extra_numbers:
            self.error(f"Unexpected skill_numbers: {sorted(extra_numbers)}")

        print()

    def _validate_dag(self):
        print("[3/4] Validating prerequisite DAG...")

        all_names = set(self.skills.keys())
        external_deps = {"agile-v-core"}  # Known external dependencies
        all_names_with_external = all_names | external_deps

        # Check all prerequisites reference valid skills
        for name, prereqs in self.adjacency.items():
            for prereq in prereqs:
                if prereq not in all_names_with_external:
                    self.error(
                        f"{name}: prerequisite '{prereq}' does not match any "
                        f"known skill name"
                    )

        # Build internal-only adjacency (exclude external deps like agile-v-core)
        internal_adjacency = {}
        for name, prereqs in self.adjacency.items():
            internal_adjacency[name] = [p for p in prereqs if p in all_names]

        # Check for cycles
        cycles = check_dag_cycles(internal_adjacency)
        if cycles:
            for cycle in cycles:
                self.error(f"Cycle detected in DAG: {' -> '.join(cycle)}")
        else:
            print("  No cycles detected.")

        # Topological sort
        topo = topological_sort(internal_adjacency, set(self.skills.keys()))
        if len(topo) == len(self.skills):
            print(f"  Topological order ({len(topo)} skills):")
            for i, name in enumerate(topo, 1):
                meta = self.skills[name].get("metadata", {})
                num = meta.get("skill_number", "?")
                group = meta.get("group", "?")
                print(f"    {i:2d}. [{num:>2}] {name} (Group {group})")
        else:
            self.error(
                f"Topological sort incomplete: got {len(topo)} of {len(self.skills)} skills "
                f"(likely due to cycles or missing nodes)"
            )

        # Verify no skill depends on a skill with a higher group
        group_order = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
        for name, prereqs in self.adjacency.items():
            my_meta = self.skills.get(name, {}).get("metadata", {})
            my_group = my_meta.get("group", "")
            for prereq in prereqs:
                if prereq in external_deps:
                    continue
                prereq_meta = self.skills.get(prereq, {}).get("metadata", {})
                prereq_group = prereq_meta.get("group", "")
                if (
                    my_group in group_order
                    and prereq_group in group_order
                    and group_order[prereq_group] > group_order[my_group]
                ):
                    self.error(
                        f"{name} (Group {my_group}) depends on {prereq} (Group {prereq_group}) "
                        f"— backward dependency across groups"
                    )

        print()

    def _validate_sequencing(self):
        print("[4/4] Validating pipeline sequencing...")

        # Check that skill_number ordering is consistent with DAG
        name_to_num = {}
        for name, data in self.skills.items():
            meta = data.get("metadata", {})
            try:
                name_to_num[name] = int(meta.get("skill_number", 0))
            except (ValueError, TypeError):
                pass

        violations = 0
        for name, prereqs in self.adjacency.items():
            my_num = name_to_num.get(name, 0)
            for prereq in prereqs:
                if prereq == "agile-v-core":
                    continue
                prereq_num = name_to_num.get(prereq, 0)
                if prereq_num >= my_num and prereq_num > 0 and my_num > 0:
                    self.warn(
                        f"Skill #{my_num} ({name}) depends on #{prereq_num} ({prereq}) "
                        f"— prerequisite has equal or higher number"
                    )
                    violations += 1

        if violations == 0:
            print(
                "  All skill_numbers are consistent with prerequisites (prereq < dependent)."
            )
        else:
            print(f"  {violations} sequencing warning(s) found.")

        # Verify fast path is a valid subset
        fast_path_nums = {1, 2, 4, 6, 10, 11, 12, 14, 15, 16, 20, 21, 24}
        num_to_name = {v: k for k, v in name_to_num.items()}
        fast_path_names = {num_to_name.get(n, f"unknown-{n}") for n in fast_path_nums}

        print(f"\n  Fast path validation ({len(fast_path_nums)} skills):")
        for num in sorted(fast_path_nums):
            name = num_to_name.get(num, "UNKNOWN")
            prereqs = self.adjacency.get(name, [])
            unmet = []
            for p in prereqs:
                if p == "agile-v-core":
                    continue
                if p not in fast_path_names:
                    unmet.append(p)
            status = "OK" if not unmet else f"WARN: needs {', '.join(unmet)}"
            print(f"    [{num:2d}] {name}: {status}")

        print()

    def _print_summary(self):
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)

        if self.errors:
            print(f"\n  ERRORS ({len(self.errors)}):")
            for err in self.errors:
                print(f"    [FAIL] {err}")

        if self.warnings:
            print(f"\n  WARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"    [WARN] {warn}")

        if not self.errors and not self.warnings:
            print("\n  All checks passed with no errors or warnings.")

        print()
        if self.errors:
            print(
                f"RESULT: FAIL ({len(self.errors)} errors, {len(self.warnings)} warnings)"
            )
        else:
            print(f"RESULT: PASS ({len(self.warnings)} warnings)")
        print()


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Validate EDA skill pipeline")
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=None,
        help="Path to domains/eda/ directory",
    )
    args = parser.parse_args()

    if args.skills_dir:
        skills_dir = args.skills_dir.resolve()
    else:
        # Default: relative to this script
        script_dir = Path(__file__).resolve().parent
        skills_dir = script_dir.parent.parent / "domains" / "eda"
        if not skills_dir.exists():
            # Try from repo root
            skills_dir = script_dir.parent / "domains" / "eda"

    if not skills_dir.exists():
        print(f"ERROR: Skills directory not found: {skills_dir}", file=sys.stderr)
        print("Use --skills-dir to specify the path to domains/eda/", file=sys.stderr)
        sys.exit(1)

    validator = SkillValidator(skills_dir)
    success = validator.validate_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
