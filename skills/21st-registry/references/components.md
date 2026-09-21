# Local component preparation

This is the component path for the active-agent adaptation. Do not run remote
component publishing, Studio checkout, or Studio rendering: automatic media
work has not been verified to avoid additional AI models. Supplying a screenshot
does not establish that all server-side media work is disabled. The limitation
does not prevent producing a complete, locally verified component bundle.

## Identify and prepare

For existing components, read inventory rather than guessing a slug:

```bash
21st components --json
21st components --status draft --scope personal --json
21st components --status published --scope team:<team-id> --json
```

Retain the returned `component:<id>` or `draft:<uuid>` reference. A login session
can see personal work and manageable teams; personal/team keys are scoped to
their respective owner. Inventory alone does not authorize checkout or upload.
Use supplied/local source or authorized catalog retrieval; do not create a
Studio revision to obtain missing code. Report when needed source is unavailable.

For new work, search for relevant existing items when catalog access is available
to reduce duplication. Inspect retrieved code and licenses before reuse. Then:

1. Prepare a self-contained component and useful demo with the active agent.
   The pinned upstream skill describes one component file and one demo as the
   supported publishing payload; do not promise support for additional local
   files or `21st.json` without checking a later version.
2. Declare imported npm packages in the appropriate package manifest. Resolve
   local/alias imports into a portable bundle. Preserve project lockfile and
   package-manager conventions; do not upload unrelated source or secrets.
3. Use portable semantic tokens such as `bg-primary`,
   `text-primary-foreground`, `bg-background`, and `border-border`. For
   Tailwind v4 custom CSS, use its mapped variables such as
   `var(--color-primary)` and `var(--color-muted-foreground)`.
4. Do not assume raw token storage formats: `oklch(var(--primary))` and
   `hsl(var(--primary))` can break when the destination stores complete colors.
   Opacity utilities such as `bg-primary/20` or `color-mix()` with mapped
   variables avoid that particular mismatch. Verify against the actual stack.
5. Build locally, open the local preview with available host browser tools,
   and exercise meaningful states in light and dark themes. Check resolved
   semantic colors, keyboard behavior, responsive layouts, and reduced motion.
6. Capture an accurate local screenshot as a proposed cover. If no browser or
   screenshot capability is available, identify the missing artifact instead
   of substituting an AI-generated illustration or claiming visual verification.

## Optional live demo controls

Upstream derives visitor controls from a module-level literal `settings` object
and a default-exported demo accepting props. Both are required for its panel.
Make every setting affect the rendered component. For example, where the
component actually supports these props:

```tsx
import { Hero } from "./Hero"

const settings = {
  headline: "Ship faster",
  showGrid: true,
  speed: 0.4,
}

export default function Demo(props: Partial<typeof settings>) {
  const s = { ...settings, ...props }
  return <Hero headline={s.headline} showGrid={s.showGrid} speed={s.speed} />
}
```

| Literal value | Upstream control |
| --- | --- |
| Number | Slider; inferred ranges need review |
| Boolean | Switch |
| CSS color string | Color picker |
| Array of up to 12 color strings | Editable palette |
| Other string up to 120 characters | Text field |
| Nested object, mixed array, long string | No control |

At most 24 controls are inferred. Keys must be plain identifiers, excluding
`key`, `ref`, `constructor`, `prototype`, and `__proto__`. Settings values must
be literals: no imported constants, computed expressions, or spreads in the
object. Expo/native demos do not get this panel. Verify changes locally through
props; do not claim the remote inferred panel has been tested.

## Deliverable

Return component/demo paths, dependency information, proposed name/slug and
accurate description, relevant existing stable ID, local cover if captured,
verification, and the remote-publishing limitation. Never fabricate a live URL.
Do not remove the restriction merely because AI access is enabled or the user
has publishing permission; the no-additional-model constraint is independent.
