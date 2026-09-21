---
name: 21st-ui-review
description: Review a web component, page, or frontend diff for design-system consistency, accessibility, responsive behavior, and interaction defects. Use for focused UI critique or requested fixes with code/runtime evidence; broader product-journey audits belong to a dedicated audit workflow.
---

# Review UI with evidence

Use the active agent and its current model for design reasoning, code generation,
iteration, and review. Do not invoke 21st hosted AI generation or iteration,
select another model, or require another AI subscription, even if the account
has AI access. This is a workflow instruction, not a change to host settings.

## Workflow

1. Read project instructions, existing design context, tokens, and the relevant
   source or diff. Establish whether the request is critique-only or includes
   fixes; a review request alone does not authorize changing the product.
2. Run existing project checks. If available and compatible with project
   network rules, add the deterministic CLI review:

   ```bash
   21st review <path> --json
   ```

   The reviewed baseline is `@21st-dev/cli` 1.17.1 (Node.js 18+); if absent,
   substitute `npx @21st-dev/cli@1.17.1` or use project lint/tests and direct
   inspection. This review uses local source rules, not another AI model or
   AI subscription. The CLI includes telemetry handling, so local analysis
   does not guarantee zero network traffic. No catalog account is required
   for these local rules.
3. Treat rule findings as candidates. Verify them against actual semantics and
   composition; regex checks cannot prove accessibility or responsive behavior.
4. Inspect runtime states with the host's available browser tools: keyboard and
   focus behavior, dialogs/menus, loading/empty/error states, overflow, relevant
   viewport sizes, reduced motion, and supported themes. If unavailable, report
   source-only findings and untested runtime risks without inventing evidence.
5. Rank proven defects by user impact with exact file/line attribution and
   reproduction steps when observed. Distinguish design-system drift,
   accessibility/interaction defects, responsive risks, and subjective design
   recommendations. Do not infer runtime behavior from component names.
6. When fixes are requested, apply narrowly justified changes. The CLI's
   `21st review <path> --fix` is limited to mechanical fixes; inspect its diff.
   Do not silently redesign or change product behavior. Run relevant checks
   and repeat affected runtime checks after fixes.

## Priorities and output

Check semantic controls and accessible names, visible focus, meaningful image
alternatives, target sizes, disabled/loading states, overflow, motion preferences,
token consistency, duplicate primitives, typography/spacing, and placeholder
content. Match findings to the task's scope.

Lead with actionable findings and evidence, then verification limits. If no
issue is proven, say so and identify what was inspected. A full product-journey
audit can use a dedicated workflow such as UXAudit when available and requested;
this skill does not require it. Do not install/update upstream skills or change
MCP configuration. See [provenance](UPSTREAM.md).
