#!/usr/bin/env python3
"""Snapshot upstream/base/local skill content for review; never edit the collection."""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit


def git(*args, cwd=None):
    try:
        return subprocess.run(
            ["git", *args], cwd=cwd, check=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=180,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        ).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        # Remote diagnostics may contain credentials; do not echo commands/stderr.
        raise ValueError("Git operation failed or timed out; check repository access and revisions") from error


def safe_path(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(p in ("..", ".git") for p in path.parts) or str(path) != value:
        raise ValueError(f"Invalid relative path: {value!r}")
    return path


def check_repository(repository):
    # Local repositories are useful for offline review/tests. Never accept an
    # arbitrary Git remote helper, option, or credential-bearing HTTPS URL.
    if Path(repository).is_absolute() and Path(repository).is_dir():
        return
    url = urlsplit(repository)
    if url.scheme == "https" and url.hostname and not url.username and not url.password and not url.query and not url.fragment:
        return
    if re.fullmatch(r"git@[A-Za-z0-9.-]+:[A-Za-z0-9_./-]+", repository):
        return
    raise ValueError("Repository must be credential-free HTTPS, git@host:path, or an absolute local directory")


def resolve_commit(repo, ref):
    if not ref or ref.startswith("-"):
        raise ValueError("Target must be a Git ref or commit, not an option")
    return git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}", cwd=repo).decode().strip()


def tree(repo, revision):
    entries = {}
    for record in git("ls-tree", "-rz", revision, cwd=repo).split(b"\0"):
        if not record:
            continue
        header, raw_path = record.split(b"\t", 1)
        mode, kind, oid = header.decode().split()
        path = raw_path.decode("utf-8")
        safe_path(path)
        entries[path] = (mode, kind, oid)
    return entries


def under(path, prefix):
    return path == prefix or path.startswith(prefix + "/")


def snapshot(repo, entries, prefixes, destination):
    destination.mkdir(parents=True)
    skipped = []
    for path, (mode, kind, oid) in entries.items():
        if not any(under(path, prefix) for prefix in prefixes):
            continue
        if kind != "blob" or mode not in ("100644", "100755"):
            skipped.append({"path": path, "mode": mode, "reason": "symlink or submodule"})
            continue
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git("cat-file", "blob", oid, cwd=repo))
    return {
        "missing_paths": [p for p in prefixes if not any(under(f, p) for f in entries)],
        "skipped": skipped,
    }


def snapshot_local(source, destination):
    destination.mkdir(parents=True)
    skipped = []
    for directory, dirs, files in os.walk(source, followlinks=False):
        for name in list(dirs):
            path = Path(directory) / name
            if path.is_symlink() or name in (".git", "node_modules", "__pycache__", ".venv"):
                dirs.remove(name)
                skipped.append(str(path.relative_to(source)))
        for name in files:
            path = Path(directory) / name
            relative = path.relative_to(source)
            if path.is_symlink() or not path.is_file():
                skipped.append(str(relative))
                continue
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
    return skipped


def inspect(root, output, selected=(), targets=None):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output == root or output.is_relative_to(root):
        raise ValueError("Report directory must be outside the collection")
    if output.exists():
        raise ValueError("Report directory already exists; choose an unused path")
    manifest = json.loads((root / "sources.json").read_text())
    sources = manifest["skills"]
    names = list(dict.fromkeys(selected)) if selected else sorted(sources)
    if not names or set(names) - sources.keys():
        raise ValueError("Select one or more imported skills recorded in sources.json")
    targets = targets or {}
    repositories = {sources[name]["repository"] for name in names}
    if targets.keys() - repositories:
        raise ValueError("A target repository does not match the selected imports")
    for name in names:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError("Invalid skill name in sources.json")
        source = sources[name]
        check_repository(source["repository"])
        if not re.fullmatch(r"[0-9a-f]{40}", source["revision"]):
            raise ValueError("Base revisions must be full commit hashes")
        if not source["paths"]:
            raise ValueError("Imported paths must not be empty")
        for path in [*source["paths"], source["local_path"], source["adaptation_notes"]]:
            safe_path(path)
        local = root / source["local_path"]
        if not local.is_dir() or local.is_symlink() or not local.resolve().is_relative_to(root):
            raise ValueError("Local skill must be a directory inside the collection")
    output.mkdir(parents=True)
    try:
        report = {"version": 1, "root": str(root), "repositories": [], "skills": []}
        report["working_tree_status"] = git("status", "--porcelain", cwd=root).decode()
        with tempfile.TemporaryDirectory(prefix="skill-upstreams-") as temp:
            for index, repository in enumerate(sorted(repositories)):
                repo = Path(temp) / str(index)
                git("clone", "--bare", "--no-local", "--", repository, str(repo))
                ref = targets.get(repository, "HEAD")
                try:
                    target = resolve_commit(repo, ref)
                except ValueError:
                    if not ref or ref.startswith("-"):
                        raise
                    git("fetch", "--no-tags", "origin", ref, cwd=repo)
                    target = resolve_commit(repo, "FETCH_HEAD")
                target_tree = tree(repo, target)
                group = [name for name in names if sources[name]["repository"] == repository]
                base_trees = {}
                for name in group:
                    base = sources[name]["revision"]
                    if base not in base_trees:
                        try:
                            resolve_commit(repo, base)
                        except ValueError:
                            git("fetch", "--no-tags", "origin", base, cwd=repo)
                            resolve_commit(repo, base)
                        base_trees[base] = tree(repo, base)
                known = [p for source in sources.values() if source["repository"] == repository for p in source["paths"]]
                exclusions = [e for e in manifest.get("excluded_skills", []) if e["repository"] == repository]
                candidates = []
                for path in sorted(target_tree):
                    if PurePosixPath(path).name != "SKILL.md" or any(under(path, p) for p in known):
                        continue
                    exclusion = next((e for e in exclusions if under(path, e["path"])), None)
                    candidates.append({
                        "path": path,
                        "status": "excluded" if exclusion else (
                            "uncollected" if any(path in t for t in base_trees.values()) else "new"
                        ),
                        "reason": exclusion["reason"] if exclusion else None,
                    })
                report["repositories"].append({"repository": repository, "requested_ref": ref, "target": target, "candidates": candidates})
                for name in group:
                    source = sources[name]
                    folder = output / name
                    entry = {"name": name, "repository": repository, "base": source["revision"], "target": target,
                             "paths": source["paths"], "local_path": source["local_path"],
                             "adaptation_notes": source["adaptation_notes"]}
                    for label, entries in (("base", base_trees[source["revision"]]), ("target", target_tree)):
                        entry[label + "_snapshot"] = snapshot(repo, entries, source["paths"], folder / label)
                    entry["local_skipped"] = snapshot_local(root / source["local_path"], folder / "local")
                    # Literal pathspecs prevent manifest filenames becoming Git patterns.
                    paths = [":(literal)" + p for p in source["paths"]]
                    diff = git("diff", "--no-ext-diff", "--no-textconv", "--binary", "--find-renames",
                               source["revision"], target, "--", *paths, cwd=repo)
                    (folder / "upstream.diff").write_bytes(diff)
                    entry["upstream_changed"] = bool(diff)
                    report["skills"].append(entry)
        (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
        return report
    except BaseException:
        shutil.rmtree(output)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument("--target", action="append", default=[], metavar="REPOSITORY=REF")
    args = parser.parse_args()
    targets = {}
    for value in args.target:
        repository, separator, ref = value.rpartition("=")
        if not separator or not repository or not ref or repository in targets:
            parser.error("Each --target must be a unique REPOSITORY=REF")
        targets[repository] = ref
    try:
        report = inspect(args.root, args.output, args.skill, targets)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f"Review failed: {error}\n")
    print(f"Compared {len(report['skills'])} skill(s): {args.output.resolve() / 'report.json'}")


if __name__ == "__main__":
    main()
