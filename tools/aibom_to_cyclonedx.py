"""Export an AI_RUN_MANIFEST as a CycloneDX 1.6 ML-BOM *view*.

Usage: python tools/aibom_to_cyclonedx.py .agile-v/aibom/<task>/AI_RUN_MANIFEST.yaml > bom.cdx.json

CycloneDX is an export, not the normative internal contract
(docs/cyclonedx-ml-bom-export.md). Confidence and evidence locators are
carried verbatim in ``agile-v:*`` properties; nothing is upgraded to
verified, and no prompt/reasoning content is exported.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml


def _props(item: dict, *extra: str) -> list[dict]:
    props = [{"name": "agile-v:confidence", "value": item.get("confidence", "unresolved")},
             {"name": "agile-v:evidence_locator", "value": item.get("evidence_locator", "")}]
    props += [{"name": f"agile-v:{key}", "value": str(item[key])} for key in extra if item.get(key) not in (None, "")]
    return props


def to_cyclonedx(manifest: dict) -> dict:
    identity, risk = manifest["identity"], manifest["risk"]
    components = []
    for model in manifest.get("models") or []:
        components.append({"type": "machine-learning-model", "name": model["name"],
                           "version": model.get("model_version") or "unknown",
                           "supplier": {"name": model["provider"]},
                           "properties": _props(model, "model_id", "inference_runtime")})
    runtime = manifest.get("agent_runtime")
    if runtime:
        components.append({"type": "framework", "name": runtime["agent_framework"],
                           "version": runtime.get("framework_version") or "unknown",
                           "properties": _props(runtime, "sandbox_image_digest", "execution_environment")})
    for tool in manifest.get("tools") or []:
        components.append({"type": "application", "name": tool["name"], "version": tool.get("version") or "unknown",
                           "properties": _props(tool, "type")})
    for skill in manifest.get("agile_v_skills") or []:
        components.append({"type": "data", "name": skill["skill"], "version": skill.get("version") or "unknown",
                           "properties": _props(skill, "source", "commit_sha")})
    return {"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1,
            "metadata": {"timestamp": identity["created_at"],
                         "tools": [{"vendor": "agile-v.org", "name": "agile-v-aibom-export", "version": "1.0"}],
                         "properties": [{"name": "agile-v:task_id", "value": identity["task_id"]},
                                        {"name": "agile-v:run_id", "value": identity["run_id"]},
                                        {"name": "agile-v:risk_level", "value": risk["agile_v_risk_level"]},
                                        {"name": "agile-v:export_kind", "value": "view-not-normative"}]},
            "components": components}


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    print(json.dumps(to_cyclonedx(yaml.safe_load(Path(argv[0]).read_text(encoding="utf-8"))), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
