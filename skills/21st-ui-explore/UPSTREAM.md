# 21st-ui-explore provenance

- Source: https://github.com/21st-dev/skill
- Pinned commit: `15c7436c41dc88c54094f1be93ce53bda456b114`
- Imported/adapted paths: `skills/21st-ui-explore/` and root `LICENSE`.
- License: Apache-2.0. Copyright 2026 21st.dev. See [LICENSE](LICENSE).
- Upstream has no separate NOTICE file at this revision.

This is a modified standalone skill in AugustoAleGon/skills, not the official
21st skill pack. Changes are recorded here as the modification notice.

## Local modifications

- Replaced hosted takes with comparable local previews and active-agent iteration. Made option count request-aware, preserved selection intent, restricted cleanup to task-created variants, and documented unavailable-preview behavior.
- Added an active-agent/current-model rule independent of account AI access;
  no provider selection, model switch, extra AI subscription, named agent, or
  plugin is required. This does not configure or enforce host runtime settings.
- Made the bundle independently usable, with portable frontmatter and relative
  resources. Sibling skill suggestions are optional.
- Added this provenance file and an unchanged copy of the upstream license.
- Corrected retained `agents/openai.yaml` invocation to `$21st-ui-explore`. No model or mandatory tool dependencies added.

## Compatibility evidence and limits

The review inspected the published `@21st-dev/cli` 1.17.1 npm artifact and
https://help.21st.dev/cli/design-runtime, https://help.21st.dev/cli/find, and
https://help.21st.dev/cli/publish. The CLI is a separate runtime dependency;
its code is not vendored into this skill. The inspected tarball integrity was
`sha512-Wx/sXQZ37pm0VAS+ll1ZkNtbn+dqy/KJbtDHjwvsdejvMaP7GNjliIrvHKDWfxBTN030Uonuzt3aDIq+aLsGdQ==`.

Design-context extraction and source-review analysis are local code. Review
includes telemetry handling, and context-aware search transmits design context.
Catalog and management operations use the remote service; we do not claim to
have audited its server internals. In particular, a supplied component cover
does not prove that Studio's automatic media pipeline avoids additional models.

Packaging/install checks are separate from real tasks executed inside a host.
No end-to-end host runtime or authenticated publishing coverage is implied.

## Updating

Fetch a desired upstream revision into a temporary directory, inspect changes
in the imported paths, and reapply the documented adaptations. Do not use the
upstream skill installer/updater to replace this modified bundle. Update the
revision and imported paths in `sources.json` and this file; preserve license
notices and rerun the collection checks. Reassess CLI/service behavior before
loosening the active-agent rule or remote component limitation.
