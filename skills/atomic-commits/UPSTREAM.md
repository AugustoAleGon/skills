# Sources and authorship

This is a locally authored skill, not an imported upstream skill. There is no
upstream Git revision or imported source path. Its original instructions and
examples are distributed under the bundled MIT license.

## References consulted

- Sandro Dzneladze, [A Developer's Guide to Atomic Git Commits](https://medium.com/@sandrodz/a-developers-guide-to-atomic-git-commits-c7b873b39223),
  published May 19, 2025; consulted November 11, 2026. Informs the focus on
  coherent changes, working intermediate revisions, useful intent, and retaining
  reviewable development commits even when the team squash-merges.
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/),
  consulted November 11, 2026. Authoritative reference for message syntax and
  breaking-change markers. The specification is licensed CC BY 3.0; the link
  identifies the original, while the bundled message guidance is a brief
  paraphrase with original examples, not a copy of the specification.

The article is linked and credited, not republished or relicensed. Source rights
remain with their respective owners. The MIT license covers this skill's
original material, not the linked publications.

## Local design

Adds agent-specific authorization boundaries, preservation of existing index
contents, staged-snapshot verification, and honest reporting. These operational
safeguards are local guidance, not requirements attributed to either source.
The skill has no runtime scripts, host-specific hooks, or required companion skills.
