# typescript-best-practices provenance

- Source: https://github.com/cursor/plugins (the `pstack` plugin).
- Pinned commit: `e5136d82418d2db3165ea1050d17577cd618cc05`.
- Imported/adapted paths:
  - `pstack/skills/typescript-best-practices/`
  - `pstack/skills/principle-type-system-discipline/SKILL.md`
  - `pstack/skills/principle-boundary-discipline/SKILL.md`
  - `pstack/LICENSE`
- License: MIT. Copyright (c) 2026 Lauren Tan. See [LICENSE](LICENSE).
- Upstream has no separate NOTICE file for `pstack` at this revision.

This is a modified standalone import in AugustoAleGon/skills. It does not
require the upstream Cursor plugin or its other skills.

## Local modifications

- Retained the TypeScript rule table and examples, subject to the corrections
  below. Removed `paths` and `disable-model-invocation` from the entry point;
  the portable description still scopes use to `.ts` and `.tsx` files and allows
  normal skill discovery and invocation across hosts.
- Bundled the two companion principles as
  [type system discipline](references/type-system-discipline.md) and
  [boundary discipline](references/boundary-discipline.md), removing their skill
  frontmatter. Replaced companion-skill mentions with relative links, including
  those in the patterns reference. Removed the optional suggestion to consult
  `encode-lessons-in-structure`; retained its schema-derivation guidance.
- Corrected the non-empty random-selection example to use tuple destructuring
  and reservoir sampling. A dynamic array index can still return `undefined`
  under `noUncheckedIndexedAccess`, even for a non-empty tuple.
- Corrected the time-range example: a plain `number` duration permits negative
  and non-finite values, so the example requires boundary validation and describes
  when a validated brand is needed.
- Added this provenance file and an unchanged copy of `pstack/LICENSE`.

## Upstream update review

Reviewed `ccb5507cec1546dc88135c1139c811e6c59115ba` →
`e5136d82418d2db3165ea1050d17577cd618cc05`. The only change in the imported paths
condenses the type-system discipline reference and folds its review questions
into the relevant rules. Adopted that revision while retaining relative links
and omitting the external `encode-lessons-in-structure` skill dependency.
Clarified the reference's duration example to match the existing boundary
validation correction in `references/patterns.md`. The rule table, patterns,
boundary reference, and MIT license are unchanged.

## Verification and limits

The bundle contains Markdown guidance and an MIT license, with no executable
scripts, plugin hooks, agent registrations, or mandatory runtime dependency.
The Zod examples illustrate using an existing schema library; installing the
skill does not install Zod or require adding it to a project.

Collection packaging and Skills CLI installation checks cover Claude Code,
Codex, and Cursor. They do not establish actual task behavior inside each host.
Upstream's plugin-manifest validation does not apply to this standalone bundle.

## Updating

Use the collection's maintenance skill to compare the pinned paths with a
desired upstream commit. Preserve the standalone references, portable entry
point, example corrections, and license. Update `sources.json` and this file
together and rerun the collection's required checks.
