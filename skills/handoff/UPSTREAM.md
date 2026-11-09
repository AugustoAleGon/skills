# Handoff provenance

- Source: https://github.com/mattpocock/skills
- Pinned commit: `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`
- Imported paths: `skills/productivity/handoff/` and repository-root `LICENSE`.
- License: MIT. Copyright (c) 2026 Matt Pocock. See [LICENSE](LICENSE).

## Local adaptations

- Added copying the complete redacted handoff text to the user's local clipboard
  after saving it. Included native command examples, quoted file-input handling,
  success reporting, and a file-preserving fallback when clipboard access fails.
- Retained temporary-file storage, next-session focus, artifact references, and
  sensitive-data redaction. Use a unique file to preserve earlier handoffs.
- Replaced the host-specific Skill tool reference with the next host's supported
  skill invocation mechanism. Preserved explicit invocation in frontmatter and
  the upstream `agents/openai.yaml` policy.
- Clipboard commands are local-only; no automatic utility installation, remote
  clipboard forwarding, previous-clipboard inspection, or new session launch.

## Verification and limits

Collection validation and installation tests check packaging and portability.
The skill has no bundled executable helper. Clipboard commands require an
available local desktop and an installed utility or host clipboard tool; they
do not establish that every host exposes clipboard access. Testing the import
must not overwrite the maintainer's clipboard.

## Updating

Use the collection maintenance workflow. Preserve the clipboard adaptation,
redaction, temporary-file fallback, and explicit invocation policy. Update the
source record and this pinned commit together.
