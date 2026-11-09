---
name: handoff
description: Compact the current conversation into a saved handoff document and copy its contents to the clipboard for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent
can continue the work. If the user passed arguments, tailor the document to that
next-session focus.

Include a "suggested skills" section naming available skills the next agent
should invoke through its host's supported mechanism.

Do not duplicate content already captured in specs, plans, ADRs, issues, commits,
or diffs. Reference them by path or URL instead.

Redact sensitive information, including API keys, passwords, and personally
identifiable information, before saving or copying the document.

## Save and copy

1. Save the redacted document to a new, uniquely named file in the user's OS
   temporary directory (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), not the
   current workspace. Do not overwrite an existing handoff.
2. Copy the complete saved document text to the user's local system clipboard,
   not just the file path or a summary. Prefer an available host clipboard tool.
   Otherwise, use an installed local clipboard command with the saved file as
   input. Quote file paths; never interpolate handoff text into shell code.

   | Local environment | Copy command |
   | --- | --- |
   | macOS | `pbcopy < "$handoff_path"` |
   | Linux / Wayland | `wl-copy < "$handoff_path"` |
   | Linux / X11 | `xclip -selection clipboard < "$handoff_path"` |
   | Linux / X11 alternative | `xsel --clipboard --input < "$handoff_path"` |
   | Windows / PowerShell | `Set-Clipboard -Value (Get-Content -LiteralPath $handoff_path -Raw -Encoding UTF8)` |

   Set `handoff_path` to the saved file's actual path using the active shell's
   syntax. Use a command for the detected local desktop, not every command in
   the table. Copying replaces the current clipboard contents; do not read or
   save the previous clipboard. Do not install clipboard utilities automatically.
3. Confirm the copy tool or command succeeded before reporting that the text was
   copied. If it fails, access is denied, or the environment is remote/headless
   without a user-local clipboard tool, keep the saved file and clearly report
   that clipboard copying was unavailable or failed. Do not use remote desktop
   clipboards or terminal clipboard escape sequences as an implicit fallback.

Finish with the handoff file path and the clipboard result so the user can
continue in a fresh session. Do not start that session automatically.
