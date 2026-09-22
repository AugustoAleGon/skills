#!/usr/bin/env python3
"""Validate the collection's portable entry points, provenance, and links."""

import ast
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def main(root=ROOT):
    root = Path(root)
    errors = []
    manifest = json.loads((root / "sources.json").read_text())
    sources = manifest["skills"]
    local_skills = manifest.get("local_skills", {})
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if sources.keys() & local_skills.keys():
        errors.append("Skill cannot have both local and imported provenance")
    for name in sources.keys() | local_skills.keys():
        if name not in {entry.parent.name for entry in skills}:
            errors.append(f"{name}: source record has no skill")
    if not skills:
        errors.append("No skills found")
    for entry in skills:
        name = entry.parent.name
        content = entry.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        if not match:
            errors.append(f"{entry}: missing frontmatter")
            continue
        fields = dict(re.findall(r"^([a-z-]+):\s*(.+)$", match[1], re.M))
        if fields.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"{entry}: invalid or mismatched name")
        if not fields.get("description"):
            errors.append(f"{entry}: missing description")
        if "allowed-tools" in fields:
            errors.append(f"{entry}: host-specific tool allowlist in portable entry point")
        source = sources.get(name, local_skills.get(name))
        if source is None:
            errors.append(f"{name}: missing sources.json entry")
            continue
        if name in local_skills:
            # Require the documented nested boolean form. Do not confuse a
            # top-level internal field or the string "true" with CLI metadata.
            metadata = re.search(r"^metadata:\s*\n((?:[ \t]+[^\n]*\n?)*)", match[1], re.M)
            internal = metadata and re.search(r"^  internal: true[ \t]*$", metadata[1], re.M)
            if source.get("internal") is not True or not internal:
                errors.append(f"{name}: local maintenance skill must have metadata.internal: true")
            if any(key in source for key in ("repository", "revision", "paths", "adaptation_notes")):
                errors.append(f"{name}: locally authored skill must not claim imported provenance")
        else:
            if not re.fullmatch(r"[0-9a-f]{40}", source.get("revision", "")):
                errors.append(f"{name}: upstream revision must be a full commit hash")
            for filename in ("LICENSE", "UPSTREAM.md"):
                if not (entry.parent / filename).is_file():
                    errors.append(f"{name}: missing {filename}")
            if source.get("adaptation_notes") != str((entry.parent / "UPSTREAM.md").relative_to(root)):
                errors.append(f"{name}: incorrect adaptation_notes")
        if source.get("local_path") != str(entry.parent.relative_to(root)):
            errors.append(f"{name}: incorrect local_path")
        for directory in (".agents/skills", ".claude/skills"):
            link = root / directory / name
            if (link.exists() or link.is_symlink()) and (
                not link.is_symlink() or link.resolve() != entry.parent.resolve()
            ):
                errors.append(f"{link}: incorrect development discovery link")

        docs = [entry]
        adapter = entry.parent / "references/host-adapter.md"
        if adapter.is_file():
            docs.append(adapter)
        for doc in docs:
            if not doc.is_file():
                errors.append(f"Missing {doc}")
                continue
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0]
                if not (doc.parent / path).exists():
                    errors.append(f"{doc}: broken reference {path}")

    # Ensure no portable dispatch points at a missing external plugin prompt.
    uxaudit = root / "skills/uxaudit"
    if uxaudit.exists():
        for doc in (uxaudit / "references/playbook").glob("*.md"):
            for role in re.findall(r'subagent_type="(uxaudit-[a-z0-9-]+)"', doc.read_text()):
                if not (uxaudit / "references/roles" / f"{role}.md").is_file():
                    errors.append(f"{doc}: missing role {role}")
        if not (uxaudit / "NOTICE").is_file():
            errors.append("uxaudit: missing upstream NOTICE")

    # Parse Python without creating caches or importing audit code.
    for directory in (root / "scripts", root / "tests", root / "skills"):
        for script in directory.rglob("*.py"):
            if "node_modules" in script.parts:
                continue
            try:
                ast.parse(script.read_text(), filename=str(script))
            except SyntaxError as error:
                errors.append(str(error))
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"Validated {len(skills)} skill(s): entry points, provenance, discovery links, roles, and Python syntax.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
