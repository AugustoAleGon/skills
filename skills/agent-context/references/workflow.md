# Discover and draft repository context

## Discover without executing

1. Establish the requested repository root and read its existing instructions.
   Inventory `AGENTS.md`, `CLAUDE.md`, README files, `docs/`, `doc/`, architecture
   documents, and ADR directories (`ADR/`, `adrs/`, `decisions/`, `doc/adr/`).
   Use the host's available file listing, search, and read capabilities.
2. Start shallow, then follow declared workspace members and module paths. Exclude
   dependency/vendor trees, generated output, caches, VCS metadata, and unrelated
   fixtures/examples from the application inventory. Report a bounded or incomplete
   scan instead of interpreting unsearched paths as absent. Do not follow symlinks
   outside the requested repository or fetch submodules automatically.
3. Read relevant manifests, selected entrypoints, sanitized config structure, schema,
   and pipeline definitions. Follow local parent manifests, version catalogs, and
   workspace dependency references; mark unresolved remote/dynamic values unknown.
   Do not evaluate executable configuration (`setup.py`, Gradle, JS config, etc.).
4. Extract purpose from the README and verified domain cues. Names alone do not
   prove business rules, table relationships, payment models, or architecture style.
5. Inventory commands from scripts, wrappers, task definitions, CI and maintained
   docs. Record each command's working directory, package manager, and evidence.
   Conflicting lockfiles or command sources remain unresolved; do not pick the
   newest-looking file. Label commands documented, not tested. Never run installs,
   code generators, migrations, or remote operations during context discovery.

## Interview only for missing context

State what was found and which files would be created. Default to augment-only,
with existing docs read-only. Ask one question at a time, and wait for the answer:

- What does the product do and who uses or pays for it, if the repository is unclear?
- Which non-obvious rules should agents know, if not already documented? Allow skip.
- Are `target-user.md` or `design.md` wanted, if the request has not specified them?
- Resolve a consequential conflicting claim or an existing target only when needed.

Do not make the user confirm every manifest. Multiple frameworks in separate
projects are not a conflict. A skipped answer stays unknown, not guessed.

## Target mapping

Read templates relative to this skill, not relative to the consumer's working directory.

| Template under `templates/en/` | Default target | Condition |
| --- | --- | --- |
| `AGENTS.md.template` | `AGENTS.md` | Missing, or explicitly authorized edit |
| `business.md.template` | `docs/business.md` | Useful business context is available |
| `architecture.md.template` | `docs/architecture.md` | No equivalent existing architecture document |
| `data-model.md.template` | `docs/data-model.md` | Verified persistence/schema evidence exists |
| `infrastructure.md.template` | `docs/infrastructure.md` | Build, CI, local services, or deployment evidence exists |
| `adrs/README.md`, `adrs/adr-template.md` | `docs/adrs/` | No existing ADR location; retain established location otherwise |
| `target-user.md.template` | `docs/target-user.md` | Requested |
| `design.md.template` | `docs/design.md` | Requested |

Create a claims ledger as described in [claim validation](claim-validation.md).
Do not create empty documents just to complete the template list. Remove placeholder
declarations and instructional examples from generated documents. Replace all
`{{UPPER_SNAKE}}` placeholders with evidence or an explicit TODO. Remove inapplicable
sections and links to omitted files; check links in every generated doc, not just AGENTS.

If AGENTS already exists, do not add pointers without authorization. Report proposed
links in the response instead. If the claims ledger exists, request an authorized
edit or a specific new filename; never silently append. Re-check target existence
and resolved path immediately before writing, including parent-directory symlinks.

## Architecture and ADRs

Give each detected project the same evidence depth: role, language, framework/library,
persistence/migrations, commands, CI and deployment configuration. Avoid inventing
layers, microservices, runtime hosting, or production topology from directory names.
Configured deployment is not observed deployment. A Dockerfile alone says nothing
about which production provider is used.

Seed at most 1–3 ADRs only when useful and supported by an existing decision or user
input. Detected technology belongs in the architecture inventory, not an invented
historical decision. A proposed ADR is labeled **Proposed**; unknown rationale,
alternatives and consequences remain **Not recorded**. Mark **Accepted** only when
an existing decision or user confirmation supports it. Use the next unused number.

## Final readback

Check the generated tree, relative links, per-project version consistency, unfilled
tokens, example entities, unsupported assertions and accidental sensitive content.
Compare authorized edits with the prior content; all other existing files stay
unchanged. Report skipped collisions and unverified claims, with no automatic commit.
