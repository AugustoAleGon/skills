# Commit messages

Read this when drafting messages. Atomicity describes the diff; a correctly
formatted subject cannot repair a mixed-purpose commit.

## Conventional Commits 1.0.0

Use `type(scope): description`, with scope optional. Insert `!` before the colon
for an incompatible change, or declare it in a `BREAKING CHANGE: explanation`
footer. Either marker suffices; a breaking change can use any type. With `!`
alone, describe the incompatibility in the subject.

Use `feat` for features and `fix` for bug fixes. Other types are allowed; follow
the repository's vocabulary. A scope names the affected area, not every file.
Separate an optional body and footer section with blank lines. Footer tokens
use hyphens instead of spaces, except `BREAKING CHANGE`; `BREAKING-CHANGE` is
also recognized. Footers accept `: ` or ` #` before their values.

The specification associates `fix`, `feat`, and breaking changes with SemVer
patch, minor, and major changes. Other types imply no version bump by themselves.
Actual releases depend on project tooling. Uppercase breaking-change footer
markers are special; the remaining syntax is not case-sensitive.

Source: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Local recommendations, not specification requirements

Prefer an imperative, concrete description and the repository's casing and
subject-length convention. Conventional Commits does not require a universal
50/72-character limit. Explain intent or tradeoffs rather than restating files.
Do not invent issue IDs, reviewers, test results, or release consequences.

Use `docs`, `test`, `refactor`, or `chore` only when that describes the unit's
purpose. Adding regression tests alongside a fix does not make it a `test` commit.
A separate refactor is useful only if it works before the behavior change.

## Original examples

A fix and its regression test form one unit:

```text
fix(cart): retain discount when removing an unavailable item

Recalculate the eligible subtotal before applying the existing discount.
```

An independent spelling correction can be another unit:

```text
docs(setup): correct the sample workspace path
```

An incompatible change needs a migration explanation:

```text
feat(config)!: require an explicit output directory

BREAKING CHANGE: outputPath is now required; set it to the previous destination
before upgrading.
```

If a proposed split has a new parser in one commit but its required helper only
in the next, move the helper earlier or combine them. Tests of the final tree
alone would miss that broken intermediate revision.
