# vercel-react-native-skills provenance

- Source: https://github.com/vercel-labs/agent-skills
- Pinned commit: `1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62`.
- Imported upstream path: `skills/react-native-skills/` (AGENTS.md, README.md, SKILL.md, metadata.json, and rules/).
- License: MIT, declared in upstream `SKILL.md` frontmatter. The repository README also declares MIT; no standalone LICENSE or NOTICE was found at the pinned revision. [LICENSE](LICENSE) records the declaration and supplies standard MIT text without inventing a copyright notice.
- Upstream author: `vercel`.

This is a modified standalone import.

## Local modifications

- Expressed upstream Markdown hard line breaks with backslashes instead of trailing spaces; rendered line breaks are preserved.

- Kept the complete rule directory, source README, skill entry point, and metadata; moved upstream `AGENTS.md` to [references/full-guide.md](references/full-guide.md) so it is an explicit resource rather than directory-scoped host instructions. Moved `metadata.json` to `references/upstream-metadata.json` because the Skills CLI excludes files named `metadata.json`.
- Updated relative rule links for the moved compiled guide.
- Added brief version/dependency compatibility guidance to the entry point; upstream examples remain guidance and do not require dependency installation or application changes.
- No upstream authoring content was omitted. The README is retained because it has no dependency on an absent build workspace.
- No scripts, plugin hooks, or repository-level agent instructions were added.

## Verification and limits

The bundle consists of Markdown and JSON. The examples mention React Native, Expo, and optional community libraries; compatibility must be checked against the consumer project's actual dependencies. No upstream checks or example snippets were executed as an app build.

## Updating

Use the collection maintenance workflow against the pinned source. Keep the compiled-guide and metadata relocations, license record, compatibility note, and standalone installation. Update this file and the collection source record together.
