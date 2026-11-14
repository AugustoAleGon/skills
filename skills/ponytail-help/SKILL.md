---
name: ponytail-help
description: "Trigger: ponytail help, how to use ponytail. Explain the six standalone skills and the limits of this collection compared with the upstream plugin."
license: MIT
metadata:
  author: DietrichGebert
  version: "1.0-local"
---

# Ponytail Help

## Activation Contract

Display this reference when asked how to use the collected Ponytail skills.
One-shot: do not edit files, change configuration, or activate a mode.

## Standalone use

Ask the agent to use a skill by its installed name, for example:
`Use ponytail-review to review my staged changes.` Use the host's supported
skill picker or invocation syntax; plugin-prefixed commands are not required.
Each skill installs independently, so check availability before suggesting a
companion workflow as runnable.

| Skill | Purpose |
| --- | --- |
| ponytail | Find the smallest complete implementation without dropping safety or checks. |
| ponytail-review | Review a change and connected code; report only. |
| ponytail-audit | Audit repository code quality; report only, not a UX audit. |
| ponytail-debt | Report shortcut comments; save a ledger only when requested. |
| ponytail-gain | Show upstream-reported benchmark results, never invented local savings. |
| ponytail-help | Explain this collection's standalone skills. |

## Guidance levels

| Level | Behavior |
| --- | --- |
| lite | Build the requested scope and name a smaller alternative. |
| full | Prefer the smallest complete change, meaningful checks, and clear limits. Default for the task. |
| ultra | Also challenge unnecessary scope before building. |

Ask for a level with the task. Say "stop ponytail" or "off" to stop applying
that guidance. This collection ships no lifecycle hooks, persistent level flags,
statusline band, automatic session activation, or plugin configuration.
It does not install or update the upstream plugin.

## Updates and limits

Use this collection's Skills CLI source for updates so local adaptations survive.
Do not run upstream plugin installers or alter host settings as part of help.
The gain card is historical upstream evidence, not a guarantee for your host.
Review and audit verdicts do not authorize edits, commits, or deployment.

## Output Contract

Give the relevant invocation example and capability limits in the user's language.
Do not imply that absent companion skills or plugin features are installed.

See [provenance and adaptations](UPSTREAM.md) for the pinned upstream source.
