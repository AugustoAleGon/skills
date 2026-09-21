---
name: 21st-design-sync
description: Extract a project's light and dark design tokens into standalone theme CSS and, when requested, publish the theme to 21st.dev. Use for preparing, sharing, or publishing a 21st theme from existing shadcn/Tailwind styles; not general component-library synchronization.
---

# Prepare and share a project theme

Use the active agent and its current model for design reasoning, code generation,
iteration, and review. Do not invoke 21st hosted AI generation or iteration,
select another model, or require another AI subscription, even if the account
has AI access. This is a workflow instruction, not a change to host settings.

## Prepare the artifact first

1. Read project instructions and locate theme variables, commonly in
   `app/globals.css`, `src/app/globals.css`, `src/index.css`, or
   `styles/globals.css`. Inspect imports and the actual theme selectors instead
   of assuming one filename or color representation.
2. Assemble a standalone CSS artifact with non-empty `:root` and `.dark`
   blocks. Preserve token names and authored values, including raw channels,
   hex, HSL, or OKLCH. Tailwind v4 `@theme inline` mappings are not the token
   values themselves; resolve references so the exported blocks are usable
   without missing project variables. Include applicable chart/sidebar/radius
   tokens and exclude unrelated CSS or private project content.
3. If dark mode is absent, prepare a proposed dark palette with the active
   agent, preserving brand hue where appropriate. Validate text/background,
   muted, accent, border, and focus combinations in a local preview; do not
   assume inverting lightness produces sufficient contrast. Keep proposed
   additions separate from the live project theme unless changing it is in
   scope. No external color skill or model is required.
4. Infer a useful name (at most 50 characters) and optional descriptive tags
   from project evidence. Present the exact file and proposed metadata. Run
   relevant CSS/build checks and inspect light/dark previews where possible;
   disclose unverified visual or contrast behavior.

## Publish only within the requested scope

Preparing CSS does not publish it. Publishing creates a public community theme;
do not assume a private publishing option. If public publication is already
clearly authorized, proceed after verification. Otherwise prepare the result
above, then ask about the concrete public action.

The reviewed CLI baseline is 1.17.1 (Node.js 18+). Use `21st` if installed or
substitute `npx @21st-dev/cli@1.17.1`. Theme management requires an API key, not
just a login session. Use an existing `TWENTYFIRST_TOKEN` / `API_KEY_21ST`
credential; never print it, embed it in arguments, or mint one automatically.
If absent, the user can obtain one at https://21st.dev/settings/api-keys.
Do not require credentials for local preparation.

```bash
21st publish-theme ./project-theme.css --name "Acme" --tags dark,minimal
```

Verify success from the service response and return the actual theme URL.
Each call creates a new theme; do not blindly retry after an ambiguous result.
Inventory/check the prior result before a retry to avoid duplicates.

## Updates

For metadata-only changes, preserve the existing theme ID:

```bash
21st edit <theme-id> --type theme --name "Updated name" --tags dark,minimal
```

Changing token values requires a new theme in the reviewed workflow. Publish
the prepared replacement only when authorized; unpublish the old theme only
when that separate removal is in scope. Theme deletion is soft unpublishing:

```bash
21st delete <theme-id> --type theme --yes
```

Do not install/update upstream skills or change MCP configuration. No sibling
skill or plugin is required. See [provenance](UPSTREAM.md).
