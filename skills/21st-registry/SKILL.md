---
name: 21st-registry
description: Prepare components for the 21st registry, publish requested themes or template listings, and manage existing catalog items or profile content. Use for explicit 21st publishing/management requests. Remote component publishing is excluded until its automatic media pipeline is verified to avoid additional model work.
---

# Prepare and manage 21st registry content

Use the active agent and its current model for design reasoning, code generation,
iteration, and review. Do not invoke 21st hosted AI generation or iteration,
select another model, or require another AI subscription, even if the account
has AI access. This is a workflow instruction, not a change to host settings.

## Route the request

- Components: follow [local component preparation](references/components.md).
  Deliver source, demo, dependency information, and a locally captured cover.
  Remote component publishing and Studio checkout/render flows are excluded
  from this adaptation: the reviewed client/docs do not establish whether the
  automatic media pipeline avoids additional model work. A supplied cover
  satisfies a cover requirement but does not prove all background work stops.
  Do not invoke those flows as a fallback or claim the component was published.
- Themes and template listings: follow [publishing and management](references/management.md).
- Inventory, metadata edits, unpublishing, catalog submissions, or profile
  changes: use the same management reference, loading only relevant sections.

## Setup and authorization

The reviewed CLI baseline is `@21st-dev/cli` 1.17.1 (Node.js 18+). Commands use
`21st`; when absent, substitute `npx @21st-dev/cli@1.17.1`. Check installed
version help for differences. Do not install globally or change MCP settings.

Component inventory and metadata management accept a saved `21st login` session
or API key. Theme/template/profile management needs an API key in the reviewed
workflow. Use existing `TWENTYFIRST_TOKEN` / `API_KEY_21ST` credentials without
printing them or passing real keys in arguments. Local preparation needs none.

Inventory existing work before changing it and retain stable identifiers.
Prepare exact artifacts and metadata before any needed approval. A request to
prepare or review does not authorize uploading, publishing, deleting, or
replacing profile content. Carry out already-authorized actions without asking
again; clarify only material target, visibility, or destructive-scope ambiguity.
Do not expose capability-bearing Studio review URLs in public logs or reports.

Report actual service results, including draft/moderation state, separately from
local preparation. On uncertain mutation outcomes, read current state before
retrying. Never treat a timeout as proof that nothing changed.

No sibling skill, plugin, or named agent is required. Do not install/update
upstream skills, which may restore hosted generation. See [provenance](UPSTREAM.md).
