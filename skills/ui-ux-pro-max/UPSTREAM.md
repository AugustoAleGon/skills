# Upstream provenance

- Repository: <https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>
- Revision: `4f2dbb67e64969a9a30ab00742f2d55d66ddec2b`
- Imported paths: `.claude/skills/ui-ux-pro-max/**`, repository-root `LICENSE`
- License: MIT; the upstream root `LICENSE` is included as `LICENSE`.

## Local adaptations

- Retained the upstream search engine, local datasets, references, fixtures, and tests from `.claude/skills/ui-ux-pro-max` as one self-contained bundle.
- Updated `SKILL.md` to invoke `scripts/search.py` from the absolute directory containing the loaded `SKILL.md`, with a quoted placeholder that supports spaces. Removed the Claude-specific `CLAUDE_PLUGIN_ROOT` assumption; no installer, user-home path, or project working-directory assumption is required.
- Narrowed skill discovery so this reference supplements an existing design system and component workflow (including 21st UI) rather than replacing them. Dedicated UX audits remain outside this reference; use dedicated UX-audit tooling if available.
- Normalized whitespace-only lines in `scripts/design_system.py`, including one blank docstring line. Verified that its Python AST is unchanged apart from that docstring whitespace; no runtime logic or output strings changed. The upstream CLI still writes only when `--persist` is passed; overwriting an existing master requires `--force`.

## Upstream repository-only tests omitted

The following upstream tests are not part of this standalone skill bundle because they depend on repository-root maintenance or whole-repository packaging tools absent from `.claude/skills/ui-ux-pro-max`. They do not test the shipped search CLI or design-system generator runtime. Runtime CLI portability is covered locally by `tests/test_ui_ux_pro_max.py`.

- `scripts/tests/test_catalog_refresh.py` — invokes repository-root `scripts/refresh-google-fonts.py` and `scripts/refresh-icon-catalog.py` to test offline catalog-generation pipelines.
- `scripts/tests/test_catalog_summary_line_endings.py` — imports repository-root `scripts/generate-catalog-summary.py` and checks generated snapshot hashes.
- `scripts/tests/test_relevance_evaluator.py` — imports repository-root `scripts/evaluate-relevance.py` and tests relevance-evaluation metrics and fixtures.
- `scripts/tests/test_skill_script_paths.py` — scans both repository-wide `.claude/skills` and `cli/assets/skills` trees and depends on the root catalog-summary generator; it is an asset-packaging check, not a runtime CLI test.

## Update history

### 2026-11-09 — `4f2dbb67e64969a9a30ab00742f2d55d66ddec2b`

Reviewed the upstream changes from `713eef51b04efc98d6fa565323b495f7c9c89fd4` and applied the compatible additions:

- Added the Apple Native Experience style row, its provenance record, and the matching active/searchable catalog counts. It is guidance for platform-aware interfaces, not a requirement to use Liquid Glass or blur.
- Added the IME Composition Enter UX guideline and provenance record, refreshed the UX count, and linked its search ID from the quick reference. The legacy `keyCode === 229` fallback remains scoped to custom web Enter shortcuts.
- Updated standalone search guidance and tests for both additions. The IME tests exercise the published CSV JavaScript example and local quick-reference entry; they do not depend on upstream repository-level docs or install tooling.

The upstream `test_ime_composition.py` repository-doc probe was adapted to inspect the bundled quick reference directly. Repository-only test modules and upstream-only relevance fingerprint fixture changes were not imported; they do not ship with this standalone bundle or validate these new skill behaviors. Existing standalone search paths, local adaptations, and persistence safeguards remain unchanged.
