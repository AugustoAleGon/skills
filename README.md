# Collected skills

My collected agent skills for **Claude Code, Codex, and Cursor**, with each self-contained
skill under `skills/<name>/SKILL.md`.

## Install

From the project where you want to use the skills:

```bash
npx skills@latest add AugustoAleGon/skills
```

Choose the skills and agents in the installer. To install every skill for all
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

UXAudit is an experimental standalone adaptation of an upstream Claude Code
plugin. It includes the seven role prompts and host instructions needed for
Claude Code, Codex, and Cursor. See [provenance and changes](skills/uxaudit/UPSTREAM.md).
Installation is tested for all three agents; full audits inside each host are
not yet verified.

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
scripts/validate.py
sources.json
tests/test_npx_install.py
.github/workflows/validate.yml
```

Optional relative links under `.agents/skills/` and `.claude/skills/` let agents
working on this collection load its skills directly. Distribution uses `skills/`
and works without those development links.

## Development

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

Third-party code retains its original license; UXAudit is Apache-2.0.
