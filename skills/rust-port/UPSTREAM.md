# rust-port provenance

- Source: https://github.com/morganlinton/BeautifulRust
- Pinned commit: `b9718436d77ee7bcf17cdcb6aa27628feb95d97a`.
- Imported paths: `skills/rust-port/SKILL.md` and repository-root `LICENSE`.
- License: MIT, copyright (c) 2026 Morgan Linton. See [LICENSE](LICENSE).

## Local adaptations

- Preserved `SKILL.md` unchanged.
- Omitted `evals/`, the `lints/` configuration, MCP server, plugin registrations, scripts, and website tooling.
- The entry point says it pairs with `rust-best-practices`. That skill is optional and installs separately; this skill works without it.
- No hooks, installers, or host configuration are imported. No named agent or model is required.

## Verification and limits

Collection tests check provenance, local references, and real Skills CLI installation.
They do not establish full host workflow coverage. The upstream benchmark and its
reported results were not reproduced here. The skills are text-only guidance; the
commands they recommend (`cargo fmt`, `cargo clippy`, `cargo test`) run only in the
user's Rust project and need a Rust toolchain.

## Updating

Update the exact commit and imported paths here and in `sources.json` together.
Keep the standalone boundary and notices. Review upstream changes before applying them.
