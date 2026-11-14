---
name: ponytail-debt
description: "Trigger: ponytail debt, list shortcuts, deferred work. Report shortcut and legacy ponytail comments as a debt ledger; persist only when requested."
license: MIT
metadata:
  author: DietrichGebert
  version: "1.0-local"
---

Every deliberate ponytail shortcut is marked with a `shortcut:` comment naming
its ceiling and upgrade path (older code may say `ponytail:`). This collects them into one ledger so a deferral
can't quietly become permanent.

## Scan

Grep the repo for comment markers, skipping `.git` and everything the
`.gitignore` files ignore (dependencies, build output, caches, in any stack):

`git grep --no-index --exclude-standard -nE '(#|//|/[*]) ?(shortcut|ponytail):'`  (add other comment prefixes if your stack uses them)

Run from the repository root. Exit code 1 means no matches; any other failure
is an unavailable scan, not a clean ledger. Git is required for this command.
For another version-control system, use an available ignore-aware search tool
and disclose any scope difference. Do not install tools automatically.

If the user names their own marker word (for example `TODO`), search for that
literal word using safely quoted arguments, not interpolated shell or regex syntax.

Each hit is one ledger row. The comment prefix keeps prose that merely mentions
the convention out of the ledger. Skip hits that are not a deferral, like a note
about a keyboard shortcut.

## Output

One row per marker, grouped by file:

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

The convention is `shortcut: <ceiling>, <upgrade path>`, so pull the ceiling
and the trigger straight from the comment. If the user asks for attribution, use `git blame -L <line>,<line> -- <file>`
with safely quoted paths. Untracked files have no blame history.

Flag the rot risk: any marker comment that names no upgrade path or
trigger gets a `no-trigger` tag, those are the ones that silently rot.

End with `<N> markers, <M> with no trigger.` Nothing found: `No shortcut debt. Clean ledger.`

## Boundaries

Reads and reports only, changes nothing. Persist only when the user requests a file (for example `PONYTAIL-DEBT.md`);
preserve existing content unless replacement is authorized. One-shot.
