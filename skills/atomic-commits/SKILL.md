---
name: atomic-commits
description: "Trigger: atomic commits, split changes, prepare commits, Conventional Commits. Plan cohesive Git commits and create them when authorized."
license: MIT
metadata:
  author: AugustoAleGon
  version: "1.0"
---

# Atomic commits

## Activation Contract

Use for planning commit boundaries, reviewing a proposed split, writing commit
messages, or creating requested commits. Do not activate merely to edit code.

## Hard Rules

- Keep planning read-only. Commit only within the user's authorized scope;
  installing or invoking this skill alone does not authorize Git mutations.
- Preserve pre-existing staged and unstaged work. Never silently unstage, stash,
  discard, amend, rebase, squash, or push. Request specific authorization when needed.
- Group one complete logical change with its necessary tests and documentation.
  Do not split by file type or target line count. Separate unrelated formatting.
- Verify each proposed commit's tree, not just the final working tree. A passing
  check that also sees later unstaged changes does not prove the commit works.
- Never bypass hooks or invent check results. Never include secrets or fabricated
  attribution; honor repository commit policy.

## Decision Gates

| Situation | Action |
| --- | --- |
| Plan or message only | Return the proposed split; do not stage or commit |
| Unrelated changes share a file | Select exact hunks, not the entire file |
| Earlier unit needs later code | Reorder or combine the dependent units |
| Existing staged work has unclear ownership | Ask before changing the index |
| Required check fails or cannot run | Report the missing proof before committing |

## Execution Steps

1. Read repository instructions and commit conventions. Inspect `git status
   --short`, `git diff`, `git diff --cached`, relevant untracked files, and recent
   commit messages. Check for an unfinished merge or rebase before mutations.
2. Describe each unit in one sentence. Identify its paths/hunks, dependencies,
   and checks. Keep each intermediate revision usable; do not claim dependent
   commits can be cherry-picked independently.
3. Read [message guidance](references/messages.md) and draft a Conventional
   Commit message for each unit. Explain non-obvious motivation in the body.
4. When authorized, stage only the selected paths or hunks. Use `git add -p`
   when interactive staging is available; otherwise use a reviewed targeted
   patch or ask for help. Do not use blanket staging on a mixed working tree.
5. Inspect the full staged diff and run `git diff --cached --check`. Verify the
   staged snapshot using repository-supported checks or a temporary isolated
   copy outside the checkout, without running checks against unrelated work.
   For documentation-only changes, use relevant structural checks.
6. Commit the verified unit. Inspect the resulting commit and remaining status;
   if hooks changed its contents, verify the changed snapshot before continuing.
   Repeat in dependency order. Preserve the team's merge strategy, including
   squash merges, rather than changing policy.

## Output Contract

For a plan, return ordered subjects, included paths/hunks, dependencies, and checks.
For execution, return created hashes and subjects, observed check results, and
remaining changes. Clearly separate proposed commits from created commits.

## References

- [Message guidance and original examples](references/messages.md)
- [Sources and local authorship](UPSTREAM.md)
