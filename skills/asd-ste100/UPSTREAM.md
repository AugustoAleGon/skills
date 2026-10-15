# ASD-STE100 provenance

- Source: https://github.com/danyuchn/asd-ste100-skill
- Pinned commit: `3944283c183eea13fe5bd902b572da3b4de8bf44`
- Imported/adapted paths: `SKILL.md`, `examples/`, `references/`,
  `scripts/`, and `LICENSE`.
- License: MIT. Copyright (c) 2026 Dustin Yuchen Teng. See [LICENSE](LICENSE).
- Upstream has no separate NOTICE at this revision.

This is a modified standalone import in AugustoAleGon/skills.

## Local modifications

- Kept the upstream name `asd-ste100`; narrowed discovery to requested technical
  rewriting. Moved upstream version `0.4.0` into portable metadata.
- Made resource links relative and clickable, and made linter invocation resolve
  from the installed skill directory instead of the consumer's working directory.
- Documented Python 3.10+, standard-library-only execution, heuristic findings,
  and the distinction between structural linting and meaning preservation.
- Corrected before/after examples: retain distinct actions, uncertainty,
  recommendation strength, and source claims. Removed added instructions and
  unsupported architecture claims. Corrected the examples' writing-rules link.
- Preserved the linter and its built-in self-tests unchanged, along with the
  intentionally invalid edge-case fixture and the writing-rules reference.
- Omitted the repository README's upstream installation instructions. This
  collection uses the Skills CLI source documented in its root README.
- Added this provenance file; preserved the upstream MIT license unchanged.

## Verification and limits

Run `python3 skills/asd-ste100/scripts/ste-lint.py --selftest` from the collection
root. Running the linter on `examples/linter-edge-cases.md` must exit 1 and report
exactly two `dangling-conjunction` findings. A nonzero exit for that fixture is
expected. Other examples intentionally contain prose that violates lint rules.

The skill does not bundle ASD's official dictionary or standard. It does not
certify STE compliance. The linter does not prove that a rewrite preserves
meaning, and synonym findings require contextual review.

Collection tests cover packaging and Skills CLI installation for Claude Code,
Codex, and Cursor. They do not establish real rewriting behavior in each host.

## Updating

Use the collection maintenance workflow against the pinned root paths. Preserve
the example corrections, portable metadata, relative links, and license. Update
this file and `sources.json` together, then run collection and linter checks.
