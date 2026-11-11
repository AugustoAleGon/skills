# Evidence-based stack inference

## Classify before naming a framework

Use three separate levels: **ecosystem/build system**, **framework/library**, and
**application role**. A package manifest establishes the first; corroborating
dependencies, plugins, configuration or source establish the others.

| Signal | Safe starting point, not a final framework claim |
| --- | --- |
| `pom.xml`, Gradle build/settings, wrappers | JVM or other Gradle/Maven build; inspect plugins/source for Java, Kotlin, Scala, Android, etc. |
| `build.sbt`, `project/build.properties` | sbt build; inspect language/framework dependencies |
| `*.csproj`, `*.fsproj`, `*.vbproj`, solutions | .NET projects; inspect SDK, target frameworks, source and project references |
| `package.json` | JS/TS package metadata; not proof of Node runtime, a web app, or a monorepo |
| `deno.json*`, `bun.lock*`, `packageManager` | Runtime/package-manager candidates; check scripts and CI for actual use |
| `pyproject.toml`, requirements, `setup.py` | Python packaging/tooling; inspect dependency groups and source without executing setup |
| `composer.json`, `Gemfile` | PHP/Ruby dependencies; not Laravel, Symfony, or Rails by default |
| `go.mod`, `go.work` | Go module/workspace metadata; inspect direct requirements and imported packages |
| `Cargo.toml` | Rust crate/workspace metadata; resolve member and workspace-inherited dependencies |
| `mix.exs`, `mix.lock` | Elixir/BEAM project; inspect each umbrella app separately |
| `pubspec.yaml` | Dart package; Flutter requires Flutter SDK evidence |
| `Package.swift`, `*.xcodeproj`, `*.xcworkspace` | Swift package or Xcode project/workspace; inspect targets/imports for platform/UI framework |
| `CMakeLists.txt`, `meson.build`, Makefiles | Build tooling, not proof of a language or framework such as Qt |

Read workspace membership (`workspaces`, `pnpm-workspace.yaml`, Maven modules,
Gradle includes, Cargo members, Go workspaces, Mix umbrella paths, project references)
and actual directories. Multiple languages alone do not prove a monorepo, and a
workspace may contain one application plus libraries. `turbo.json` or `nx.json`
indicates tooling; describe the observed projects rather than asserting organization.

## Confirm each claim at its owning root

- Follow manifest/config declarations into a small representative source sample.
  Record app, library, plugin, example and tooling roles separately. A peer dependency
  or transitive lockfile entry is not proof the repository runs that framework.
- Inspect both runtime and development/build dependencies: framework compilers such
  as Astro or SvelteKit can legitimately be dev dependencies. Dependency placement
  alone neither confirms nor rejects application use.
- Record declared constraints as constraints (`^5`, version ranges, BOM inheritance),
  not installed versions. Lockfiles establish a recorded resolution, not what is
  running in production. Scope several resolved versions to the correct project.
  Unresolved aliases, catalogs or dynamic versions stay unknown.
- Follow configured route/source/schema roots; conventional filenames are examples,
  not mandatory layouts. Absence of a default path does not prove absence of a tool.
- Prefer evidence of actual source use over stale copied config. State contradictions
  and scan limits. Use [framework signals](framework-signals.md) only as a lookup;
  for unlisted or version-sensitive frameworks, consult their official documentation.

## Keep adjacent concerns separate

| Concern | Evidence to inspect | Do not conclude |
| --- | --- | --- |
| Persistence | ORM/driver dependencies plus schema/model/config references | A database engine, live connection, or hosting provider from an ORM name alone |
| Migrations | Flyway/Liquibase/Alembic/Prisma/Drizzle or native framework configuration and actual migration files | Django implies Alembic; Laravel implies Doctrine; a directory name proves migrations execute |
| Containers | Dockerfile stages, Compose YAML services | Containers are deployed, or local Compose reflects production |
| Kubernetes/Helm | `apiVersion`/`kind`, chart metadata, Kustomize resources | `values.yaml`, `k8s/`, or generic YAML alone proves Kubernetes |
| IaC | Terraform resources, Bicep, CDK dependency/config, Serverless provider or SAM transform | `template.yaml` alone proves AWS SAM; `.tfvars` values are safe to read |
| CI/CD | Workflow jobs, triggers, referenced scripts and deployment steps | Workflow presence means passing builds or active production deployment |
| API contracts | OpenAPI version/content, protobuf services, WSDL definitions | Every `.proto` uses gRPC or every `.xsd` exposes SOAP |
| Quality checks | Scripts/CI invoking tools; ESLint flat config, Ruff, Checkstyle, RuboCop, etc. | `.editorconfig` or an unused linter config proves an enforced CI quality gate |

Record only safe variable names and redacted structural details. Do not inspect
actual secret-bearing config to settle an inference. Use sanitized examples,
manifests and source references; ask or mark uncertainty when these are insufficient.
