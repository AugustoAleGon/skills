#!/usr/bin/env python3
"""Validate the collection's portable entry points, provenance, and links."""

import ast
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    sources = json.loads((ROOT / "sources.json").read_text())["skills"]
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
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
        source = sources.get(name)
        if source is None:
            errors.append(f"{name}: missing sources.json entry")
            continue
        if not re.fullmatch(r"[0-9a-f]{40}", source.get("revision", "")):
            errors.append(f"{name}: upstream revision must be a full commit hash")
        if source.get("local_path") != str(entry.parent.relative_to(ROOT)):
            errors.append(f"{name}: incorrect local_path")
        for filename in ("LICENSE", "UPSTREAM.md"):
            if not (entry.parent / filename).is_file():
                errors.append(f"{name}: missing {filename}")
        for directory in (".agents/skills", ".claude/skills"):
            link = ROOT / directory / name
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
    uxaudit = ROOT / "skills/uxaudit"
    if uxaudit.exists():
        for doc in (uxaudit / "references/playbook").glob("*.md"):
            for role in re.findall(r'subagent_type="(uxaudit-[a-z0-9-]+)"', doc.read_text()):
                if not (uxaudit / "references/roles" / f"{role}.md").is_file():
                    errors.append(f"{doc}: missing role {role}")
        if not (uxaudit / "NOTICE").is_file():
            errors.append("uxaudit: missing upstream NOTICE")

    # Parse Python without creating caches or importing audit code.
    for directory in (ROOT / "scripts", ROOT / "tests", ROOT / "skills"):
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
