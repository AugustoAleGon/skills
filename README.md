# Collected skills

Agent skills for **Claude Code, Codex, and Cursor**. Each bundle lives in
`skills/<name>/` and can be installed on its own.

## Install

Run this command from the project where you want to use the skills:

```bash
npx skills@latest add AugustoAleGon/skills
```

Choose skills and agents in the installer. Installation requires Node.js/npm
and Git.

### Install one skill

Select just one skill by name, then choose its target agents in the installer:

```bash
npx skills@latest add AugustoAleGon/skills --skill atomic-commits
```

Replace `atomic-commits` with any name in the table below. To install only that
skill for Codex without prompts:

```bash
npx --yes skills@latest add AugustoAleGon/skills --skill atomic-commits --agent codex --yes
```

### Install all public skills

To install all public skills for all three agents without prompts:

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
| [atomic-commits](skills/atomic-commits/SKILL.md) | Split changes into complete logical commits and write Conventional Commit messages |
| [agent-context](skills/agent-context/SKILL.md) | Generate repository context with evidence-backed framework inference |
| [handoff](skills/handoff/SKILL.md) | Save a redacted conversation handoff and copy its text to the local clipboard |
| [asd-ste100](skills/asd-ste100/SKILL.md) | Clarify technical English while preserving meaning and uncertainty |
| [vercel-react-best-practices](skills/vercel-react-best-practices/SKILL.md) | Apply 70 React and Next.js performance rules |
| [vercel-react-native-skills](skills/vercel-react-native-skills/SKILL.md) | Apply React Native and Expo performance and interface guidance |
| [vercel-composition-patterns](skills/vercel-composition-patterns/SKILL.md) | Design composable React component APIs and state boundaries |
| [web-design-guidelines](skills/web-design-guidelines/SKILL.md) | Review UI code against freshly retrieved Vercel interface guidelines |
| [writing-guidelines](skills/writing-guidelines/SKILL.md) | Review prose against freshly retrieved Vercel writing guidelines |
| [ui-ux-pro-max](skills/ui-ux-pro-max/SKILL.md) | Search local UI/UX guidance, palettes, typography, and stack-specific patterns |
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

- **Atomic commits:** Requires Git for inspection and committing. Planning is
  read-only; creating commits requires authorization. It does not push or rewrite
  history implicitly. See [sources and authorship](skills/atomic-commits/UPSTREAM.md).
- **Agent context:** Explicitly invoked; generates Markdown context.
  Preserves existing docs unless specific edits are authorized. Its framework
  reference guides evidence-based inference, not automatic detection or runtime
  verification. See [framework sources](skills/agent-context/references/framework-signals.md)
  and [provenance](skills/agent-context/UPSTREAM.md).
- **Handoff:** Explicitly invoked. Saves to the OS temporary directory and copies
  the complete redacted document using an available local clipboard tool or
  native utility. Copying replaces clipboard contents; if unavailable, the file
  remains available. No clipboard utility is installed automatically.
- **ASD-STE100:** The optional linter requires Python 3.10+ and no third-party
  packages. The skill omits ASD's official dictionary and does not certify STE
  compliance. See [provenance](skills/asd-ste100/UPSTREAM.md).
- **React and TypeScript:** The guidance has no runtime dependencies. Use the
  target project's versions and libraries. Measure performance in that project.
- **Web and writing guidelines:** Require network access through the host's web
  or HTTP tool to fetch the current review criteria. They do not bundle an offline
  copy or certify compliance when retrieval is unavailable.
- **UI/UX Pro Max:** Requires Python 3.10+; its local search uses only the standard
  library. Resolve script paths from the loaded skill directory, not the project
  working directory. Design-system persistence is opt-in; overwrites require
  explicit authorization. It supplements existing design systems and workflows.
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
python3 skills/ui-ux-pro-max/scripts/validate_data.py
python3 -m unittest discover -s skills/ui-ux-pro-max/scripts/tests -v
```

Installation tests use Node/npm and network access to resolve `skills@latest`.
They run in temporary projects, outside personal agent directories. CI also
checks JavaScript syntax. Test local installation from a separate project,
using this checkout's absolute path as the source.

## Sources and licenses

[sources.json](sources.json) records upstream repositories, exact commits,
imported paths, local skills, and exclusions. Each imported bundle includes
`UPSTREAM.md` with adaptations and a `LICENSE` file.

Locally authored skills use `local_skills` with an explicit `internal` boolean:
`false` for public skills and `true` for maintenance-only skills. They do not
claim upstream Git revisions. Atomic commits is original MIT-licensed guidance
informed by the sources linked in its provenance document.

UXAudit and the 21st skills use Apache-2.0. The other public skills use MIT.
Vercel declares MIT in its repository README and selected skill metadata. The local
[license record](skills/vercel-react-best-practices/LICENSE) documents the absence
of a standalone upstream license file; the new Vercel bundles record the same
repository-wide declaration at their pinned revision.
