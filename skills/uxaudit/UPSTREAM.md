# UXAudit provenance

- Source: https://github.com/gotalab/uxaudit
- Pinned commit: `36244e37c96405715e5e7397d5752a431bc61c77`
- Imported: `skills/uxaudit/`, seven `agents/uxaudit-*.md` prompts, `LICENSE`, and `NOTICE`.
- License: Apache-2.0. Copyright 2026 gotalab. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

This is a locally adapted standalone skill, not the official Claude plugin.
Upstream advertises Claude Code only. Codex and Cursor portability comes from
this collection's instructions and still requires full host testing.

Local modifications:

- `SKILL.md`: shared frontmatter, narrower discovery description, host-adapter
  entry point, portable role paths, and accurate isolation/model guidance.
- `references/host-adapter.md`: host tool mapping, explicit fresh-context role
  dispatch, capability limits, and evidence isolation guidance.
- `references/playbook/`: standalone dependency/path setup and portable dispatch
  guidance replacing plugin auto-loading and provider-specific model assumptions.
- `references/roles/`: bundled upstream prompts without Claude registration
  frontmatter; clarified actual isolation and model reporting where applicable.
- `LICENSE`, `NOTICE`, and this provenance file added to the standalone bundle.

The catalog, detectors, schemas, capture scripts, dashboard, and dependency
lockfile are preserved from the pinned revision. Plugin hooks and marketplace
metadata are not required for this standalone installation.

To update, fetch the desired revision into a temporary directory, review changes
to the imported paths, reapply the documented adaptations, retain license/notice,
update `sources.json` and this file, and run repository checks. Do not replace
this folder wholesale without reviewing the adaptations.
