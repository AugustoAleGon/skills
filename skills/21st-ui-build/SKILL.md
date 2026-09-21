---
name: 21st-ui-build
description: Build or substantially change web UI using the project's design system and useful 21st component inspiration. Use for pages, sections, components, responsive redesigns, or visual polish with an established direction. Implement with the active agent's current model.
---

# Build project-aware UI

Use the active agent and its current model for design reasoning, code generation,
iteration, and review. Do not invoke 21st hosted AI generation or iteration,
select another model, or require another AI subscription, even if the account
has AI access. This is a workflow instruction, not a change to host settings.

## Workflow

1. Read project instructions, the target route and nearby components, tokens,
   and existing `.21st/design.json` / `.21st/DESIGN.md` when present. Explicit
   project facts take precedence over generic design taste.
2. If persistent design context would help, the reviewed CLI 1.17.1 can extract
   it locally with `21st init --design-context`. If the CLI is absent, use
   `npx @21st-dev/cli@1.17.1 init --design-context` (Node.js 18+) or inspect the
   sources directly. CLI setup and a 21st account are not required to build UI.
   Preserve authored constraints and decisions; use `--check` to detect drift
   and `--refresh` only when intentionally refreshing extracted facts.
3. Reuse project primitives first. When catalog inspiration helps, use
   `21st search "<specific UI need>" --type component --limit 5 --json`, then
   `21st get <id> --json` for promising code. Use a saved login or an existing
   environment credential without displaying it. Retrieval may be metered.
   Omit `--context auto` by default: it uploads design context; evaluate fit
   locally. Inspect retrieved code, dependencies, and license before reuse.
   If the service is unavailable, continue from project components.
4. Implement directly with the active agent in the project's real framework.
   When no catalog item fits, create the implementation yourself. Preserve
   established APIs; do not paste standalone sketch HTML into a component app.
   If the direction is undecided, present a few grounded alternatives first;
   the optional `21st-ui-explore` skill offers a fuller workflow.
5. Preserve responsive behavior, semantic controls, keyboard access, visible
   focus, reduced motion, and loading/empty/error states. Use real product copy
   and assets where available. Avoid decorative effects unsupported by the
   project or request.
6. Run relevant project checks. If available, `21st review <changed-paths>` adds
   deterministic source checks; it does not prove runtime accessibility or
   visual correctness. CLI 1.17.1 includes telemetry handling despite local
   analysis. Respect project network rules and use project checks instead when
   appropriate. Inspect actual UI states at relevant viewport sizes with the
   host's available browser tools; report source-only coverage if unavailable.
7. Record an accepted durable visual decision in existing project design notes.
   If using `.21st/design.json`, preserve its schema and unrelated entries;
   decision entries have `id` and `decision`, with optional `createdAt`/`source`.
   Keep `.21st/DESIGN.md` consistent if maintained.

## Handoff

Report the implemented direction, reused components, changed files, checks,
and runtime limitations. Do not install/update upstream skills, change MCP
configuration, or publish artifacts as a side effect. No sibling skill, plugin,
or named agent is required. See [provenance](UPSTREAM.md).
