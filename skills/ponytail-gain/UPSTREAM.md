# ponytail-gain provenance

- Source: https://github.com/DietrichGebert/ponytail
- Pinned commit: `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`.
- Imported paths: `skills/ponytail-gain/SKILL.md`, `LICENSE`, `benchmarks/results/2026-10-07-agentic.md`.
- License: MIT. Copyright (c) 2026 DietrichGebert. See [LICENSE](LICENSE).

## Local adaptations

- Normalized portable discovery metadata; `1.0-local` identifies this adaptation,
  not an upstream release version.
- Bundled the cited benchmark report under references/benchmark.md and changed its reproduction link to the pinned upstream URL. Numbers are upstream-reported, not independently reproduced; documented shell-disabled and partial-correctness coverage and no generalization to this adaptation. No benchmark scripts imported or run; sibling skills are optional.
- Imported skills only, not the upstream root agent rules, plugins, hooks,
  installers, or host configuration. No named agent or model is required.

## Verification and updates

Collection tests cover packaging, independent installation, and local references.
They do not establish full host workflow coverage or reproduce benchmark results.
Keep these adaptations during updates; update this revision and sources.json together.
