# Phase 00 — Environment setup

Local adaptation; see [UPSTREAM.md](../../UPSTREAM.md).
Read [the host adapter](../host-adapter.md) before this phase.
**Next phase:** [01-discovery.md](01-discovery.md).

## Resolve the loaded bundle

Set `UXAUDIT_DIR` to the absolute directory containing the loaded `SKILL.md`,
resolving any symlink. Use the path supplied by host skill discovery. An explicit
user-provided `UXAUDIT_DIR` is supported; verify it contains this bundle's
`SKILL.md`, `package.json`, `scripts/`, and `references/roles/`. Do not depend on
`CLAUDE_PLUGIN_ROOT`, `CLAUDE_PLUGIN_DATA`, or a plugin hook.

```bash
# Substitute the actual resolved path; this is an example, not a literal path.
export UXAUDIT_DIR="/absolute/path/to/skills/uxaudit"
export UXAUDIT_LANG="en"  # ja only when requested with --lang ja
```

Keep the working directory in the audited project. If the host starts a fresh
shell for each call, supply the environment again or use absolute script paths;
exports do not necessarily persist between tool calls. Quote paths.

## Dependencies

Use Node.js 20+ with npm, and Python 3.10+. Python scripts use the standard
library. Install the locked Node dependencies and Chromium before first use:

Check the interpreter version before running scripts. If `python3` is older
than 3.10, use an installed newer interpreter (such as `python3.14`) consistently
for every Python command in the playbook; do not modify the system Python.

```bash
npm ci --prefix "$UXAUDIT_DIR" --ignore-scripts
node "$UXAUDIT_DIR/node_modules/playwright/cli.js" install chromium
```

Skip installation when the locked dependencies and matching Chromium are already
present. Use normal host network/filesystem permissions; report failed setup.
Dependencies live beside the bundle so ES module imports work without
`NODE_PATH`. Playwright uses its normal per-user browser cache. Linux hosts may
need Playwright's documented OS dependencies; do not assume permission to install
system packages.

## Artifacts

Per-project runs default to `.agents/uxaudit/<target>/`. Ignore that subdirectory
if audit output should stay local; do not ignore `.agents/skills/`.
`UXAUDIT_HOME` optionally overrides the global report library/registry. Without
an override, scripts use existing XDG/default `~/.agents/uxaudit` behavior.
Use a temporary `UXAUDIT_HOME` for tests to avoid modifying the user's library.
