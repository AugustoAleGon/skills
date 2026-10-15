# Collected skills

Agent skills for **Claude Code, Codex, and Cursor**. Each bundle lives in
`skills/<name>/` and can be installed on its own.

## Install

Run this command from the project where you want to use the skills:

```bash
npx skills@latest add AugustoAleGon/skills
```

Choose skills and agents in the installer. Installation requires Node.js/npm
and Git. To install all public skills for all three agents without prompts:

```bash
npx --yes skills@latest add AugustoAleGon/skills --skill '*' --agent claude-code codex cursor --yes
```

Use `--skill <name>` to select a skill, `--list` to list skills, or `--global`
to install across projects. Use `--copy` if your system cannot create symlinks.
Review prompts before replacing existing skills.

The [Skills CLI](https://github.com/vercel-labs/skills) copies bundles into your
project and manages installation and updates. Codex and Cursor use
`.agents/skills/`. Claude Code uses links under `.claude/skills/`. Installation
does not install each skill's runtime dependencies or log into services.

## Skills

| Skill | Purpose |
| --- | --- |
| [asd-ste100](skills/asd-ste100/SKILL.md) | Clarify technical English while preserving meaning and uncertainty |
| [vercel-react-best-practices](skills/vercel-react-best-practices/SKILL.md) | Apply 70 React and Next.js performance rules |
| [typescript-best-practices](skills/typescript-best-practices/SKILL.md) | Model types, validate boundaries, and derive types from schemas |
| [uxaudit](skills/uxaudit/SKILL.md) | Audit usability, accessibility, interface quality, and user journeys |
| [21st-cli-use](skills/21st-cli-use/SKILL.md) | Find, retrieve, and install 21st catalog items |
| [21st-ui-build](skills/21st-ui-build/SKILL.md) | Build UI with project components and design tokens |
| [21st-ui-explore](skills/21st-ui-explore/SKILL.md) | Create and compare local UI options |
| [21st-ui-review](skills/21st-ui-review/SKILL.md) | Review frontend code and runtime behavior |
| [21st-design-sync](skills/21st-design-sync/SKILL.md) | Prepare light/dark theme CSS and publish it when requested |
| [21st-registry](skills/21st-registry/SKILL.md) | Prepare components locally and manage themes, template listings, and metadata |

Ask the agent to use a skill by name. For example:

```text
Use asd-ste100 to clarify this tool description without changing its meaning.
Use vercel-react-best-practices to review this page's loading performance.
Use 21st-ui-build to implement this pricing page with our existing components.
```

Codex also supports `$skill-name` invocation. Each skill includes its own
instructions, examples, and links to further guidance.

## Requirements and limits

- **ASD-STE100:** The optional linter requires Python 3.10+ and no third-party
  packages. The skill omits ASD's official dictionary and does not certify STE
  compliance. See [provenance](skills/asd-ste100/UPSTREAM.md).
- **React and TypeScript:** The guidance has no runtime dependencies. Use the
  target project's versions and libraries. Measure performance in that project.
- **UXAudit:** Requires Node.js 20+, Python 3.10+, Playwright Chromium, image
  viewing, and fresh subagent contexts. Start the app's development server first.
  Reports default to `.agents/uxaudit/`. See [setup and host requirements](skills/uxaudit/SKILL.md).

Invoke standalone UXAudit with `/uxaudit`, rather than the upstream plugin's
`/uxaudit:uxaudit`:

```text
Claude Code / Cursor: /uxaudit my-app --url http://localhost:3000
Codex:               $uxaudit my-app --url http://localhost:3000
```

The six **21st skills use the active agent's current model**. They exclude
hosted `21st-ai` and require no second AI subscription or model switch. Local
UI work can proceed without a 21st account. These skills do not change host
model settings or disable other tools.

Catalog and management operations use `@21st-dev/cli` 1.17.1 with Node.js 18+.
Catalog access may require authentication and has account-dependent retrieval
limits. Theme, template, and profile management requires an API key.
The CLI includes telemetry. `search --context auto` sends project design
context to the service, so these skills default to ordinary search.

Remote component publishing, Studio checkout, and Studio rendering remain
excluded because the automatic media pipeline may use additional AI models.
Theme publication is public. Template listings enter moderation. See
[21st workflow details and limits](skills/21st-registry/UPSTREAM.md).
Use this collection's installer source for updates to preserve these adaptations.

Installation tests cover all three agents. Full host workflows, authenticated
catalog operations, and publishing remain unverified. UXAudit is an experimental
standalone adaptation. Report partial coverage when required host tools are missing.

## Maintain the collection

Use [update-collected-skills](skills/update-collected-skills/SKILL.md) to check
upstreams or apply reviewed updates. New skills require explicit scope to add them.
The maintenance skill is internal and excluded from normal listing and bulk
installation. Explicit selection can still install it.

Keep one canonical bundle under `skills/<name>/`. Optional relative links in
`.agents/skills/` and `.claude/skills/` support development in this checkout.
See [AGENTS.md](AGENTS.md) for contribution rules and required checks.

Run checks with Python 3.10+ (`python3.14` on the maintainer's Mac):

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
python3 skills/uxaudit/scripts/validate_checks.py
python3 skills/uxaudit/scripts/test_checks.py
python3 skills/asd-ste100/scripts/ste-lint.py --selftest
```

Installation tests use Node/npm and network access to resolve `skills@latest`.
They run in temporary projects, outside personal agent directories. CI also
checks JavaScript syntax. Test local installation from a separate project,
using this checkout's absolute path as the source.

## Sources and licenses

[sources.json](sources.json) records upstream repositories, exact commits,
imported paths, local skills, and exclusions. Each imported bundle includes
`UPSTREAM.md` with adaptations and a `LICENSE` file.

UXAudit and the 21st skills use Apache-2.0. The other public skills use MIT.
Vercel declares MIT in its skill metadata. Its local
[license record](skills/vercel-react-best-practices/LICENSE) documents the absence
of a standalone upstream license file.
