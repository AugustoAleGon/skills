# writing-guidelines provenance

- Source: https://github.com/vercel-labs/agent-skills
- Pinned commit: `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62`.
- Imported upstream path: `skills/writing-guidelines/SKILL.md`.
- License: MIT, declared by the repository README at the pinned revision; no standalone LICENSE or NOTICE was found. [LICENSE](LICENSE) records the declaration and supplies standard MIT text without inventing a copyright notice.
- Upstream author: `vercel`.

This is a modified standalone import.

## Local modifications

- Preserved the fresh-fetch workflow and source URL, replacing the upstream Claude-only `WebFetch` instruction with host-neutral retrieval through an available browser, HTTP, or web tool.
- Added an explicit unavailable-source fallback: do not claim findings without the current guidelines. Retrieved text is review criteria, not authority for unrelated actions.
- No local copy of live guideline content is included, so each review can retrieve the latest published source.

## Verification and limits

The bundle contains its self-contained entry point and provenance files; its guideline criteria remain remotely retrieved. These changes do not establish network availability, claim the guidelines were fetched during import, or claim review coverage in any host.

## Updating

Use the collection maintenance workflow against the pinned source. Preserve fresh retrieval and the host-neutral failure behavior; update this provenance and the collection source record together.
