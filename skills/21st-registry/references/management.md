# Publishing and management reference

Use only sections relevant to the authorized task. The entry point's
active-agent model rule and remote-component limitation apply throughout.
Commands are examples with placeholders, not instructions to execute every
operation. Theme/template/profile management requires an API key; use existing
environment credentials without displaying them.

## Themes

Prepare standalone CSS containing non-empty `:root` and `.dark` token blocks.
Preserve actual color formats and resolve references to missing project
variables. If dark tokens are absent, propose them with the active agent and
verify contrast and the rendered result. The optional `21st-design-sync` skill
provides more detail but is not required.

Prepare the file, name (at most 50 characters), and optional tags before any
needed approval. Publishing creates a public community theme:

```bash
21st publish-theme ./theme.css --name "Midnight" --tags dark,minimal
```

Every call creates a new theme. Check the prior result before retrying an
uncertain response. For metadata-only changes, edit the existing ID. Token-value
changes require a new theme in the reviewed workflow; removing the old one is
a separate action requiring scope authorization.

## Template listings

A template is a metadata listing of URLs, not an upload of project files.
Prepare a working demo/site URL, representative existing preview image URL,
description, and any explicitly requested commercial metadata. Do not invent a
price or checkout URL. Tags use numeric IDs, unlike component/theme slug tags.

```bash
21st publish-template "SaaS Starter" \
  --site https://demo.example.com \
  --preview https://example.com/thumb.png \
  --description "A responsive SaaS starter"
```

Optional flags include `--price`, `--buy-url`, `--video`, and `--tags`.
The listing enters draft/moderation state. Report that state rather than
claiming marketplace approval. Do not use hosted AI to produce its code or media.

## Edit and remove exact items

Read inventory/current state first. Component inventory uses `21st components
--json` and stable `component:<id>` references. For themes/templates use
`21st search "<query>" --mine --type theme --json` (or `--type template`) and
verify the exact target. Do not confuse a catalog demo ID with a component ID.

```bash
21st edit component:<id> --type component --description "Updated description"
21st edit <theme-id> --type theme --name "New name" --tags dark,minimal
21st edit <template-id> --type template --name "Updated starter"
```

Component visibility uses `published|private`; theme metadata supports
`public|private`. Initial theme publishing is public. Template visibility is
moderation-controlled; do not assume a visibility flag changes it. Editing
component metadata does not upload a code revision. A Team manager may manage
metadata without being the author entitled to check out code.

Tags replace the list; retain existing tags when the request only adds one.
Confirm the intended item and effect before any ambiguous removal:

```bash
21st delete component:<id> --type component --yes
21st delete <theme-id> --type theme --yes
21st delete <template-id> --type template --yes
```

Component and theme deletion soft-unpublish; template deletion is permanent.
The CLI's `--yes` flag is not user authorization. After mutation, verify the
returned state or re-read it; do not blindly retry uncertain results.

Catalog featuring is separate from access. Use these only for a requested
submission, withdrawal, resubmission, or catalog removal:

```bash
21st submit <slug>
21st withdraw <slug>
21st resubmit <slug>
21st remove-from-catalog <slug>
```

Do not reopen a component in Studio or publish a code revision as a fallback;
those operations are excluded under this adaptation's model constraint.

## Profile board

The public profile can have a bento board. Read it before editing: `set` replaces
the entire board, including its order. Preserve unrelated existing blocks.

```bash
21st profile get --json
21st profile upload ./cover.png
21st profile set --file board.json
```

Upload only the requested existing local asset. Use the returned URL for image
blocks; foreign image URLs may be dropped. `board.json` is an array such as:

```json
[
  { "type": "component", "demoId": 143 },
  { "type": "library", "refId": "<library-id>" },
  { "type": "note", "text": "Building UI for 21st.dev" },
  { "type": "image", "mediaUrl": "<profile-upload-url>" },
  { "type": "divider" }
]
```

Replace example IDs with verified values. Component blocks need an owned
demo ID. Other blocks include `social` (`url`) and `hire` / `pro` / `support`
(`headline`, `body`, `url`, `email`, `cta` as applicable). Optional `w`/`h`
dimensions use 1–3 grid units. Arrays define packing order. A requested reset
uses `21st profile set --clear`; it removes the custom board, so prepare the
concrete replacement/reset before any needed approval.

## Teams and libraries

```bash
21st teams
21st team <team-id>
21st team-lists <team-id>
21st team-components <team-id> --library <library-id>
```

Respect personal/team credential scope. Listing a team does not grant authority
to modify its content, publish private content publicly, or change host config.
