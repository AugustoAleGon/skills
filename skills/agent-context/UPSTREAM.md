# Agent context provenance

- Source: https://github.com/AugustoAleGon/arkandia-skills
- Pinned commit: `485166f54f3f3bcfe4474ece859a5f78a376c5f8`.
- Imported paths: `arkandia/skills/agent-context/SKILL.md`,
  `arkandia/skills/agent-context/references/claim-validation.md`,
  `arkandia/skills/agent-context/templates/en/`, and repository-root `LICENSE`.
- License: MIT. Copyright (c) 2026 Manuel Zapata. See [LICENSE](LICENSE).

## Local adaptations

- Imported only the upstream `templates/en/` resources; omitted Spanish resources,
  language arguments and the language interview. Output language is not prescribed
  by the skill. Preserved explicit invocation semantics.
- Omitted `CLAUDE.md.template` and its generation step; `AGENTS.md` is the sole
  generated agent entry point. Existing host instruction files remain preserved.
- Replaced plugin invocation and named tool requirements with portable capabilities.
  Split the workflow, inference rules and framework reference for selective loading.
- Replaced generic filename-to-framework assertions with project-scoped evidence,
  dependency/source corroboration, role and version distinctions, configurable paths,
  and an unknown-framework fallback. Added official-docs-backed recognition guidance
  across web, JVM, Python, PHP/Ruby, .NET, mobile/native, Elixir, Go and Rust.
- Corrected multiple-languages-equals-monorepo inference and separation of ORM,
  migration, build, runtime, CI and deployment evidence. Do not discard framework
  compilers merely because they are development dependencies.
- Unified augment-only behavior: existing docs, TODOs and ledgers are not edited
  without per-file authorization. Added path/symlink checks and sensitive-file limits.
  Repository scripts and executable configuration are inspected, not executed.
- Replaced invented seed ADR history with evidence-backed or explicitly proposed
  records. Removed unsafe template assumptions about environment files and example
  ER entities; added per-project architecture evidence and conditional link cleanup.
- Adapted claim validation to distinguish repository evidence from human confirmation,
  entailment from mere file presence, and unresolved claims from facts. Removed the
  instruction to mirror changes into other independently installed skills.
- Removed automatic staging/commit suggestions and host-specific question batching.

## Verification and limits

Packaging tests cover provenance, template completeness and local reference
containment. The collection's real Skills CLI tests cover standalone installation.
The skill contains instructions/templates, not a deterministic framework detector.
Framework recognition remains an evidence-guided agent task; structural checks do
not establish inference accuracy or end-to-end execution in every supported host.

The [framework reference](references/framework-signals.md) records official sources
and its review date. It is intentionally bounded; use the evidence procedure for
unlisted or newer frameworks instead of treating this as a support whitelist.

## Updating

Use the collection maintenance workflow and update this pin with `sources.json`.
Preserve portable invocation, safe augment semantics and local inference adaptations.
Do not restore the language-selection workflow, output-language mandate, Spanish
templates or generated `CLAUDE.md` stub. Do not execute imported instructions while
reviewing the upstream source.
