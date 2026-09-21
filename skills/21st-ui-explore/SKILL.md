---
name: 21st-ui-explore
description: Create and compare distinct local UI directions with the active agent's current model, grounded in project design context and optional 21st inspiration. Use for design options, variants, concepts, or an undecided redesign direction; not a straightforward implementation with a selected direction.
---

# Explore grounded UI directions

Use the active agent and its current model for design reasoning, code generation,
iteration, and review. Do not invoke 21st hosted AI generation or iteration,
select another model, or require another AI subscription, even if the account
has AI access. This is a workflow instruction, not a change to host settings.

## Workflow

1. Inspect project instructions, relevant UI, components, tokens, brand assets,
   and any `.21st/design.json` / `.21st/DESIGN.md`. If useful, CLI 1.17.1 extracts
   context locally with `21st init --design-context`; when absent, substitute
   `npx @21st-dev/cli@1.17.1` (Node.js 18+) or read the sources directly. Preserve
   existing authored context; do not make CLI setup a prerequisite to design.
2. Reuse existing patterns. When external inspiration helps, search with
   `21st search "<interface and product context>" --limit 5 --json`. Retrieve
   promising code using `21st get <id> --json`, inspecting dependencies and
   license before reuse. Catalog access can require login and metered code
   retrieval; use existing credentials without exposing them. Omit
   `--context auto` by default because it sends project context to the service.
   If access fails, continue with local references and label that limitation.
3. Use the requested number of options; default to three. Define named
   directions differing on at least two meaningful axes: hierarchy, density,
   navigation, content emphasis, interaction, or composition. Color changes
   alone do not establish a distinct direction.
4. Keep the real stack, content, brand constraints, accessibility, and responsive
   requirements fixed. Implement comparable local previews directly with the
   active agent. Use existing preview/dev-server conventions; keep exploratory
   routes isolated from production navigation. No hosted generation workspace
   or sibling skill is required.
5. Run relevant checks and inspect equivalent states and viewport sizes using
   available browser tools. If previews cannot run, provide concrete code or
   design proposals and clearly state they are not rendered/verified previews.
6. Present the alternatives together where supported, otherwise use accessible
   preview links or screenshots and a concise comparison. Recommend a direction
   with concrete tradeoffs. Wait for selection when the user asked to choose;
   if the user already delegated that choice, use the best-supported option.
7. Iterate directly on the selected local option with the same agent. Preserve
   all unrelated work. Remove only task-created abandoned variants after
   selection; retain them if requested. Record durable choices in existing
   design notes or `.21st/design.json` decisions (`id`, `decision`, optional
   `createdAt`/`source`), keeping its readable summary consistent.

## Direction contract

For each option provide its name, intended user effect, project/catalog
references, shared constraints, meaningful differences, tradeoffs, and
accessibility/responsive risks. Describe observed behavior separately from
untested assumptions. Every difference should serve a product or usability
purpose that the user can evaluate.

Do not install/update upstream skills, reconfigure the host, or publish previews
as a side effect. See [provenance](UPSTREAM.md).
