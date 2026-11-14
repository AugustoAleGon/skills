# ponytail-help provenance

- Source: https://github.com/DietrichGebert/ponytail
- Pinned commit: `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`.
- Imported paths: `skills/ponytail-help/SKILL.md`, `LICENSE`.
- License: MIT. Copyright (c) 2026 DietrichGebert. See [LICENSE](LICENSE).

## Local adaptations

- Normalized portable discovery metadata; `1.0-local` identifies this adaptation,
  not an upstream release version.
- Replaced plugin-specific reference card with independently installed skill guidance. Retained six capabilities and lite/full/ultra intent; omitted persistent flags, statusline/band, host configuration, global upgrades and plugin update commands that this collection does not provide.
- Imported skills only, not the upstream root agent rules, plugins, hooks,
  installers, or host configuration. No named agent or model is required.

## Verification and updates

Collection tests cover packaging, independent installation, and local references.
They do not establish full host workflow coverage or reproduce benchmark results.
Keep these adaptations during updates; update this revision and sources.json together.
