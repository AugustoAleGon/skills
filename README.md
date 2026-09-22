# Collected skills

My collected agent skills for **Claude Code, Codex, and Cursor**, with each self-contained
skill under `skills/<name>/SKILL.md`.

## Install

From the project where you want to use the skills:

```bash
npx skills@latest add AugustoAleGon/skills
```

Choose the skills and agents in the installer. To install every public skill for all
three agents without prompts:

```bash
npx --yes skills@latest add AugustoAleGon/skills --skill '*' --agent claude-code codex cursor --yes
```

Add `--global` to make them available across your local projects. Installation
uses the standard [Skills CLI](https://github.com/vercel-labs/skills) and requires
Node.js/npm and Git. No Python installer, local clone, or npm package publication
is needed. The GitHub commands require this collection to be pushed to the
repository first.

Install only UXAudit, or list the collection before installing:

```bash
npx skills@latest add AugustoAleGon/skills --skill uxaudit
npx skills@latest add AugustoAleGon/skills --list
```

The CLI copies the skill bundle into the destination project and sets up agent
links. Codex and Cursor use `.agents/skills/`; Claude Code gets a link under
`.claude/skills/`. Use `--copy` if your environment cannot create symlinks. Review
existing-skill replacement prompts before accepting them. The CLI manages
installation and updates; `sources.json` separately tracks the upstream code
collected here.

## Skills

| Skill | What it does | Source |
| --- | --- | --- |
| [uxaudit](skills/uxaudit/SKILL.md) | Audits usability, accessibility, interface quality, and user journeys; produces evidence and ranked fixes | [gotalab/uxaudit](https://github.com/gotalab/uxaudit) |
| [21st-cli-use](skills/21st-cli-use/SKILL.md) | Finds, retrieves, and installs 21st catalog items for adaptation by the active agent | [21st-dev/skill](https://github.com/21st-dev/skill) |
| [21st-ui-build](skills/21st-ui-build/SKILL.md) | Implements project-aware UI with the active agent's current model | [21st-dev/skill](https://github.com/21st-dev/skill) |
| [21st-ui-explore](skills/21st-ui-explore/SKILL.md) | Creates and compares local UI directions with the active agent | [21st-dev/skill](https://github.com/21st-dev/skill) |
| [21st-ui-review](skills/21st-ui-review/SKILL.md) | Reviews a component, page, or frontend diff with source/runtime evidence | [21st-dev/skill](https://github.com/21st-dev/skill) |
| [21st-design-sync](skills/21st-design-sync/SKILL.md) | Prepares light/dark theme CSS and publishes it when requested | [21st-dev/skill](https://github.com/21st-dev/skill) |
| [21st-registry](skills/21st-registry/SKILL.md) | Prepares components locally and manages themes, template listings, and registry/profile metadata | [21st-dev/skill](https://github.com/21st-dev/skill) |

UXAudit is an experimental standalone adaptation of an upstream Claude Code
plugin. It includes the seven role prompts and host instructions needed for
Claude Code, Codex, and Cursor. See [provenance and changes](skills/uxaudit/UPSTREAM.md).
Installation is tested for all three agents; full audits inside each host are
not yet verified.

## Use the adapted 21st skills

These six skills are modified imports pinned to upstream commit
[`15c7436c41dc88c54094f1be93ce53bda456b114`](https://github.com/21st-dev/skill/tree/15c7436c41dc88c54094f1be93ce53bda456b114).
The hosted `21st-ai` skill is excluded. Design reasoning, generation, variants,
iteration, and critique use the **active agent's current model**, regardless of
the account's 21st AI access. No second AI subscription, provider selection,
named subagent, or plugin is required by these skills. They do not change the
host's model settings or technically disable other installed tools.

Install the six skills, or select any one independently:

```bash
npx skills@latest add AugustoAleGon/skills --skill 21st-cli-use 21st-ui-build 21st-ui-explore 21st-ui-review 21st-design-sync 21st-registry
npx skills@latest add AugustoAleGon/skills --skill 21st-ui-build
```

Example requests:

```text
Use 21st-ui-build to implement this pricing page with our existing components.
Use 21st-ui-explore to show three local dashboard directions.
Use 21st-ui-review to review this frontend diff without changing files.
Use 21st-cli-use to find a suitable 21st navigation component.
Use 21st-design-sync to prepare our light/dark theme CSS for review.
Use 21st-registry to prepare this component and its demo locally.
```

Codex also supports explicit `$21st-ui-build`-style invocation. Each bundle is
self-contained; sibling skill suggestions are optional. Build, explore, review,
and theme/component preparation can proceed without a 21st account. Previews
use the target project's framework, dev server, and available browser tools.
Missing browser capabilities must be reported as unverified runtime coverage.

Catalog and management operations use `@21st-dev/cli` (reviewed baseline
**1.17.1**, Node.js 18+). If the CLI is absent, the skills use
`npx @21st-dev/cli@1.17.1` for relevant operations. Skills installation does not
install that runtime or log in. Catalog access may require authentication and
has account-dependent code retrieval limits; these are separate from AI
generation. If access fails, ordinary UI work can continue locally. Keep keys
in existing environment credentials or use a saved login where supported.
Theme/template/profile management requires an API key in the reviewed workflow.

Project design-context extraction and UI rule analysis are local code, but
the CLI has telemetry handling. `search --context auto` sends design context
to the service, so the adapted skills default to ordinary search and local
fit assessment. No zero-network or server-internals guarantee is implied.

**Component publishing limitation:** the reviewed client/docs do not establish
whether Studio's automatic cover/video pipeline avoids additional AI models.
This adaptation therefore supports local component/demo/cover preparation but
excludes remote component publishing, Studio checkout, and Studio rendering.
A supplied cover is not proof that all background model work is disabled.
Theme publication, template listings, and metadata/profile changes remain
available within the user's authorized scope. Theme publication is public;
template listings initially enter moderation. See the
[registry provenance](skills/21st-registry/UPSTREAM.md) and each skill's
`UPSTREAM.md` for exact adaptations.

Use this collection's Skills CLI source for installation and updates, not the
upstream 21st skill installer/updater, which distributes different workflows.
Installation checks cover the complete collection and individual skills for
Claude Code, Codex, and Cursor. They do not establish end-to-end host behavior
or authenticated catalog/publishing coverage.

## Use UXAudit

In the project being audited, start your development server and invoke:

```text
Claude Code / Cursor: /uxaudit my-app --url http://localhost:3000
Codex:               $uxaudit my-app --url http://localhost:3000
```

Or ask: “Use the uxaudit skill to audit this app at http://localhost:3000.”
This standalone skill uses `/uxaudit`, not the plugin's `/uxaudit:uxaudit`.

Running an audit additionally requires **Node.js 20+, Python 3.10+, and
Playwright Chromium**, plus image viewing and fresh subagent contexts. The skill
includes first-use dependency setup instructions; `npx skills add` installs the
skill files, not its browser/runtime dependencies. Project reports default to
`.agents/uxaudit/`. Report partial coverage when host capabilities are missing.

## Repository structure

```text
skills/
  uxaudit/
    SKILL.md
    references/
    scripts/
    checks/
    schemas/
    templates/
    LICENSE
    NOTICE
    UPSTREAM.md
  21st-cli-use/
  21st-ui-build/
  21st-ui-explore/
  21st-ui-review/
  21st-design-sync/
  21st-registry/
    SKILL.md
    references/
    LICENSE
    UPSTREAM.md
scripts/validate.py
sources.json
tests/test_npx_install.py
.github/workflows/validate.yml
```

Optional relative links under `.agents/skills/` and `.claude/skills/` let agents
working on this collection load its skills directly. Distribution uses `skills/`
and works without those development links.

## Development

For maintenance in this checkout, invoke `$update-collected-skills`, or ask the
agent to use `skills/update-collected-skills/SKILL.md`. For example:

```text
Use update-collected-skills to check all tracked upstreams and report new candidates.
Use update-collected-skills to update uxaudit while preserving our local adaptations.
```

The helper creates base/upstream/local snapshots and a comparison report in a
new directory outside the checkout. Check mode leaves tracked files untouched;
update mode applies reviewed changes and runs validation. Newly discovered skills
are candidates until additions are in scope. `sources.json` records imported
provenance under `skills`, locally authored maintenance skills under `local_skills`,
and intentional upstream exclusions under `excluded_skills`.

The canonical maintenance skill lives at `skills/update-collected-skills/`, with
relative development links like the public skills. Its `metadata.internal: true`
excludes it from ordinary Skills CLI listing and bulk installation. Explicit
selection or `INSTALL_INTERNAL_SKILLS=1` can still install it; this is not access
control or a promise that the source is private. It is omitted from the public
skill catalog above. Integration tests verify the normal export boundary.

Add a self-contained directory at `skills/<name>/`, with `name` and `description`
frontmatter in `SKILL.md` and relative resource paths. Preserve third-party
licenses/notices, pin imports in [sources.json](sources.json), and document local
adaptations. Skills CLI discovers new skill folders automatically.

Before publishing, test this checkout from a different project by replacing the
GitHub source with its absolute local path:

```bash
npx skills@latest add /absolute/path/to/this/collection --skill uxaudit --agent claude-code codex cursor
```

Do not install the collection into itself with the CLI: its development links
already point to the source folders. The integration test installs into a
separate temporary project, verifies all runtime files for all three agents,
and checks that the installation survives removal of its source clone.

Run checks with Python 3.10+ (on this Mac, use `python3.14` in place of `python3`):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 skills/uxaudit/scripts/validate_checks.py
python3 skills/uxaudit/scripts/test_checks.py
```

The integration test requires Node/npm and network access to resolve
`skills@latest`; it does not install into your personal agent directories.
GitHub Actions runs these checks plus JavaScript syntax checks.

Third-party code retains its original license; UXAudit and the imported 21st
skills are Apache-2.0. Each imported skill includes its own license and
provenance record. The separate 21st CLI is not vendored here.
