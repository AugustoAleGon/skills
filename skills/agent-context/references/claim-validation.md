# Validate load-bearing claims

Adapted from the upstream Claimify-inspired procedure. This is a lightweight
documentation check, not a Claimify implementation or proof of runtime behavior.

1. Select roughly 8–15 consequential claims: per-project framework/version,
   persistence, migrations, configured deployment/CI, commands and their working
   directories, domain relationships and user-supplied invariants.
2. Split each into one self-contained statement. Attach a repository `file:line`
   source or clearly attributed user statement; a filename alone does not entail
   its presumed framework. Distinguish a version constraint from a locked resolution.
3. Assign **high** confidence only when evidence entails the whole claim; **medium**
   for indirect/partial evidence; **low** for unsupported hypotheses. Source presence
   is not enough: a Dockerfile does not entail an AWS production deployment.
4. Resolve contradictions and consequential ambiguity with one focused question at
   a time, then wait. Do not ask users to reconfirm directly supported, nonconflicting
   facts. User-confirmed business rules are attributed policy, not code verification.
5. Remove or mark unanswered claims `<!-- TODO: verify -->`; do not assert them in
   architecture, ADRs or diagrams. Apply corrections consistently across documents.
6. Persist the ledger at an authorized path. Default to `docs/claims-ledger.md` only
   if absent; otherwise request an authorized edit or a specific unused filename.

```markdown
# Claims ledger

| Claim | Source | Confidence | Status |
| --- | --- | --- | --- |
| The service targets Java 21. | pom.xml:14 | high | repository-verified |
| Production runs on AWS. | inferred | low | unverified; omitted from docs |
| Tenant filtering is required. | user confirmation | high | user-confirmed policy |
```

Use distinct statuses: **repository-verified**, **user-confirmed**, **corrected**,
or **unverified**. Never label a file-backed fact human-confirmed unless the user
actually confirmed it. Existing ledgers and documentation remain read-only without
specific edit authorization. Do not mirror changes into other skills automatically.
