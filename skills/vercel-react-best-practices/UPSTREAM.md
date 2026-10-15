# Vercel React best practices provenance

- Source: https://github.com/vercel-labs/agent-skills
- Pinned commit: `063bee94c3f4df8453406c830b0a7df0f2860278` (resolved from `main`).
- Imported/adapted path: `skills/react-best-practices/`.
- License: MIT, declared in upstream `SKILL.md` frontmatter.
- Upstream author: `vercel`; organization: Vercel Engineering.
- Upstream has no standalone LICENSE or NOTICE at this revision. [LICENSE](LICENSE)
  records the declaration and supplies standard MIT text locally, without
  inventing an upstream copyright notice.

This is a modified standalone import in AugustoAleGon/skills.

## Local modifications

- Used the upstream frontmatter name `vercel-react-best-practices` for the local
  directory. Kept the 70 rule files and two rule-authoring resources. Moved
  `metadata.json` to `references/upstream-metadata.json` because the Skills CLI
  excludes files named `metadata.json` during installation.
- Relocated the compiled `AGENTS.md` to
  [references/full-guide.md](references/full-guide.md), so a reference document
  does not become directory-scoped host instructions. Adjusted relative rule
  links for the new location and linked it from `SKILL.md`.
- Added project-version, measurement, dependency, and behavior-preservation
  guidance to the entry point. Rule examples are context-dependent guidance,
  not a requirement to add packages or change application behavior.
- Omitted the upstream authoring README: its commands depend on the separate
  `packages/react-best-practices-build/` workspace, which is not a runtime
  dependency and is not distributed with this skill.
- Added the license record and this provenance file. No other skills, plugin
  hooks, archives, or upstream repository instructions are imported.

## Verification and limits

The bundle contains Markdown and JSON and has no executable runtime dependency.
Examples refer to project libraries such as React, Next.js, SWR, `better-all`,
and `lru-cache`; installing the skill does not install those packages.

The upstream rule validator lives at
`packages/react-best-practices-build/src/validate.ts`. Run it in an isolated
snapshot of that workspace with the imported rules at
`skills/react-best-practices/rules/`, after reviewing its code. Collection checks
also verify installation and resource preservation for Claude Code, Codex, and
Cursor. These checks do not compile every illustrative snippet, substantiate
performance figures, or establish application behavior inside each host.

## Updating

Use the collection maintenance workflow against the pinned skill directory.
Keep the directory-name mapping, compiled-reference relocation, license
declaration, and standalone installation. Update this file and `sources.json`
together. Recheck the upstream license if a standalone file is added later.
