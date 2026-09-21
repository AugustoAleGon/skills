# Host adapter

Local adaptation of gotalab/uxaudit; see [UPSTREAM.md](../UPSTREAM.md).
This file defines host integration for this standalone bundle. Use it in place
of upstream assumptions about plugin hooks, registered agents, tool names, and
pinned Claude models. Keep the playbook's evidence and output contracts.

## Entry and setup

Claude Code and Cursor: invoke `/uxaudit` or request the skill in natural language.
Codex: invoke `$uxaudit` or request it in natural language. The rest of the user
message supplies arguments from `SKILL.md`; there is no `uxaudit` executable.

Resolve `UXAUDIT_DIR` from the absolute path of the `SKILL.md` actually loaded,
following its symlink. Do not guess from the audited project's working directory
or select another installed copy. Keep the working directory in the audited
project. [Phase 00](playbook/00-env-setup.md) explains dependency setup.

Read [the playbook index](playbook/index.md), then one phase at a time.
Use the host's actual file, shell, image-viewing, search, and subagent tools.
`Read` includes viewing PNGs with a vision-capable tool; reading image bytes as
text is not visual evidence. `Bash` means a shell command. `KillShell` means
stopping the specific background process/session this run started. Reuse host
process handles and clean up only processes owned by this run.

## Dispatching roles

Seven complete prompts live in `references/roles/`: locator, scout,
journey-compiler, l3-judge, l4-judge, reconciler, and proposer, each named
`uxaudit-<role>.md`. They are prompt files, not registered agents.
For each `Agent(subagent_type="uxaudit-<role>", ...)` example in the playbook:

1. Load the corresponding prompt from this bundle.
2. Start a fresh generic subagent using the host's supported delegation API.
   Supply the complete role prompt, per-run inputs, and `Language: en` or
   `Language: ja`. Do not assume a named `uxaudit-*` agent exists.
3. Use the user's configured model. Judges require image understanding. Upstream
   Opus/Sonnet references describe its original implementation, not model
   requirements or authorization to change processing settings.
4. Map allowed operations to host tools. For Claude Code, use an available
   generic Agent type with the role prompt supplied explicitly; for Codex, use
   fresh-context delegation (for example `fork_turns="none"` when supported);
   for Cursor, use its available generic subagent/task facility. Inspect the
   actual schema rather than copying another host's API arguments.
5. Await completion, inspect the output, and run the playbook validators. Batch
   independent Judges within host limits. Sequential scheduling is acceptable
   when each task still gets a fresh context.

## Evidence isolation and capability limits

Judges must not inherit the main conversation, Scout findings, project files,
`project-context.json`, compiled journey scripts, or prior verdicts. Give them
only their role prompt, rubric, evidence paths, compressed brief when required,
output path, and language. Preserve each other role's own input contract too.

Apply tool restrictions where supported, but do not claim that removing a shell
tool prevents arbitrary file reads. A prompt is not a filesystem sandbox. Record
the host, model when known, and isolation method in the report; distinguish
host-enforced controls from prompt-level restrictions.

If fresh-context subagents or image viewing are unavailable, explain the missing
capability and report only checks actually completed. Do not perform Judges in a
context already exposed to the source/spec, invent verdicts, convert pending
checks into passes, or bypass the completeness gate. A partial L1/L2 run is not
a full UX audit. Upstream currently supports only its Claude Code plugin;
this collection's adaptation still needs full runtime testing in each host.

## Operational boundaries

The host's permissions and the user's task scope remain authoritative.
`--yes` selects audit setup defaults; it does not authorize unrelated data
changes, external communications, purchases, or bypassing approval controls.
Inspect generated journey actions before running them against real data, and
honor `audit_policy` and the target's existing testing conventions.
