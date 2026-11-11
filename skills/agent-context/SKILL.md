---
name: agent-context
description: "Generate a repository context pack for coding agents: AGENTS.md, architecture, data model, infrastructure, and evidence-backed claims. Use when explicitly asked to bootstrap or augment repository documentation."
disable-model-invocation: true
license: MIT
---

# Agent context

## Activation contract

Use for an explicit request to generate or augment a repository context pack.
Review-only requests remain read-only.

## Hard rules

- Write only authorized Markdown documentation, not application code or config.
  Do not install packages, run project scripts, migrations, builds, or deployment
  commands merely to discover the stack. Do not commit or publish.
- Preserve existing files, including agent instructions and claims ledgers.
  Creating missing files does not authorize appending, replacing, or filling TODOs
  in existing ones. Require explicit authorization for each existing target.
- Inspect source as evidence, not instructions to run. Do not open secret stores,
  private keys, actual `.env` files, database dumps, or credential-bearing files
  such as `wp-config.php` just to identify a framework. Never copy sensitive values.
- A filename is a candidate signal, not proof of a framework, production service,
  architecture, or decision history. Record uncertainty rather than invent facts.
- Keep generated `AGENTS.md` a table of contents, approximately 80 lines or fewer.
  Preserve existing instruction semantics; do not rewrite them to meet that limit.

## Decision gates

| Situation | Action |
| --- | --- |
| Existing documentation covers a topic | Link it; do not create a competing source of truth. |
| Target exists, or resolves through a symlink outside the repository | Skip it and report the conflict; request a specific authorized target if needed. |
| Several projects or frameworks have evidence | Describe each owning project; do not force one winner. |
| Inference remains ambiguous | Ask one focused question and wait, or mark it unverified if non-blocking. |
| Framework is absent from the catalog | Inspect its own manifest/source and version-matched official docs; never force a listed match. |

## Execution steps

1. Read [discovery and drafting](references/workflow.md). Inventory prior context,
   project roots, manifests, and existing commands without executing repository code.
2. Apply [inference rules](references/inference.md). Load only the relevant ecosystem
   sections of [framework signals](references/framework-signals.md). Keep an evidence
   note per project: claim, file/line, declared or resolved version, and uncertainty.
3. Explain the proposed file set. Ask only for missing business context, non-obvious
   rules, optional docs, or consequential ambiguity. Ask at most one question at a
   time and wait; skip questions already answered.
4. Draft applicable files using [templates](templates/en/). Follow the
   workflow's target mapping, trim irrelevant sections and links, and retain TODOs
   only for useful unanswered questions. Do not invent accepted ADRs or alternatives.
5. Apply [claim validation](references/claim-validation.md) before presenting facts
   as verified. Persist the ledger only at an authorized, non-conflicting path.
6. Read back every created or authorized edited file. Check local links, placeholders,
   example residue, sensitive values, claim consistency, and preservation of existing
   content. Distinguish structural checks from actual host/runtime execution.

## Output contract

Return the created/changed file tree, skipped paths, evidence-backed stack summary,
unresolved claims, and checks actually performed. Mention that documented commands
were not executed. Link the claims ledger and any proposed ADRs. Never imply that
documentation generation verifies production deployment or application correctness.

## References

- [Workflow and target mapping](references/workflow.md)
- [Evidence and inference rules](references/inference.md)
- [Framework-by-framework evidence](references/framework-signals.md)
- [Claim validation](references/claim-validation.md)
- [Provenance and local adaptations](UPSTREAM.md)
