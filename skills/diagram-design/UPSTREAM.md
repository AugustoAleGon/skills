# Diagram Design provenance

- Source: https://github.com/cathrynlavery/diagram-design
- Pinned commit: `f6db0decea96de66b901331a0f79a8d4b147ebae`.
- Imported paths: `skills/diagram-design/`, repository-root `LICENSE`, and
  `THIRD_PARTY_LICENSES.md`.
- License: MIT, copyright (c) 2025 Cathryn Lavery. See [LICENSE](LICENSE).
  Retained [third-party notices](THIRD_PARTY_LICENSES.md) describe the icon sources
  and their separate licenses and trademarks. Their upstream repository paths are
  attribution context, not dependencies on files in this collection.

## Local adaptations

- Preserved the complete standalone bundle: references, templates, examples,
  fixtures, and all eight Python helpers. Helper code and assets are unchanged.
- Added installation-root path resolution, standalone invocation, dependency,
  browser-input safety, and network/offline guidance to the entry point.
- Qualified animation checks that require upstream repository-only scripts;
  documented the packaged self-check and manual browser checks instead.
- Clarified that natural-language export does not require plugin slash commands.
- Omitted repository plugin registrations, commands, hooks, website, and
  maintainer tooling. No dependency installation or host configuration occurs
  when importing this skill.
- Preserved onboarding consent, profile handling, and the installed-skill
  diagnostic mode. Retained upstream design rules and style-guide setup choices.

## Verification and limits

Collection tests check provenance, local reference containment, real Skills CLI
installation, and representative valid/invalid self-check inputs. Python syntax
validation covers the bundled helpers. These checks do not establish full host
workflow, browser rendering, profile persistence, PNG export, or all import-format
coverage. The maintainer checks mentioned in upstream references are not bundled.

HTML/SVG generation is text-based. Python helpers require Python 3.10+; PNG export
requires Playwright and a compatible Chromium installation. Default templates can
fetch Google Fonts when rendered. Offline use requires system-font output and
the packaged `self_check.py --offline` check, not merely a local HTML file.

## Updating

Update the exact commit and imported paths here and in `sources.json` together.
Preserve the standalone boundary, notices, explicit network consent, and honest
verification limits. Review executable helpers and HTML before running them;
importing upstream content is not permission to execute its instructions.
