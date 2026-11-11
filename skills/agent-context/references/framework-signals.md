# Framework signals and official references

Reviewed 2026-11-11. Read only sections relevant to detected projects. This is a
bounded recognition catalog, not an exhaustive support list or a version matrix.
The official docs support package/config conventions; the caveats are inference
rules for this skill. Verify version-specific behavior against the target project's
version, not the documentation site's current default.

Combine positive signals at the owning project root. A dependency alone can denote
a library, integration, example or test rather than an application. A missing default
path is not negative proof. Apply [inference rules](inference.md) before using a row.

## Web UI and full-stack JavaScript

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| React | [Docs](https://react.dev/learn/installation) | `react` and usually `react-dom` declared in the app package manifest; JSX/React entrypoint corroborates. | React is a UI library, not proof of an application framework; React may be a component embedded in another app. |
| React Router framework mode | [Docs](https://reactrouter.com/start/framework/installation) | `react-router` plus `@react-router/dev` / framework config or generated `app/routes.*`; CLI uses `create-react-router`. | `react-router` can be used in library/data-router modes, not only full-stack framework mode. Legacy Remix v2 manifests use `@remix-run/*`; inspect project generation/config rather than assuming migration. |
| Nuxt | [Docs](https://nuxt.com/docs/4.x/examples/hello-world) | `nuxt` in package dependencies and `nuxt.config.*`, with Nuxt app conventions (e.g., `app.vue`, `pages/`). | Nuxt modules may bring Nuxt dependencies; check the app root/config. Older docs/versions differ, and a package entry alone may be module/tooling code. |
| Astro | [Docs](https://docs.astro.build/en/install-and-setup/) | `astro` in package dependencies, usually `astro.config.*`, `src/pages/`, and `astro dev/build` scripts. | Astro can be declared under `devDependencies` because it is a build framework; do NOT discard it as tooling-only. A standalone integration package can depend on Astro without being an Astro app. |
| Next.js | [Docs](https://nextjs.org/docs/app/getting-started/installation) | Direct `next` package plus Next scripts and app/pages routing source; inspect project configuration. | React or `app/` alone is not Next.js. Confirm App Router, Pages Router or mixed usage from source. |
| Angular | [Docs](https://angular.dev/reference/configs/workspace-config) | Angular dependencies plus workspace project targets and Angular source; `angular.json` identifies CLI workspace configuration. | A workspace may contain libraries; inspect project type/build targets. AngularJS is a different framework. |
| Vue | [Docs](https://vuejs.org/guide/quick-start.html) | `vue` dependency or a verified browser import plus Vue component/application source. | Vue may be embedded or used under Nuxt; Vite alone does not establish Vue. |
| Svelte | [Docs](https://svelte.dev/docs/svelte/overview) | Svelte dependency/compiler integration and `.svelte` components. | Svelte components do not imply SvelteKit, SSR, or a standalone application. |
| SvelteKit | [Docs](https://svelte.dev/docs/kit/project-structure) | `@sveltejs/kit`, Svelte config and Kit routing/build integration; default route root is `src/routes`. | Check configurable paths and adapters. SvelteKit packages may be dev dependencies; Svelte alone is insufficient. |

## JavaScript servers

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| NestJS | [Docs](https://docs.nestjs.com/first-steps) | `@nestjs/core` in the app manifest plus `NestFactory` bootstrap; `nest-cli.json` corroborates. | Workspace packages can include Nest support libraries without being the runnable Nest app; identify the owning package. |
| Express | [Docs](https://expressjs.com/en/starter/installing.html) | `express` dependency plus an Express app/router entrypoint. | A custom script can use Express without making the whole repository an Express service. |

## JVM

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| Quarkus | [Docs](https://quarkus.io/guides/getting-started/) | Maven/Gradle build includes `io.quarkus:quarkus-bom`, `quarkus-maven-plugin`, Quarkus extension dependencies, or Gradle Quarkus plugin. | `pom.xml`/Gradle alone only indicate build system; a parent BOM or plugin can be shared in a multi-module build, so inspect module-level deps. |
| Micronaut | [Docs](https://docs.micronaut.io/4.10.x/gradle/) | Gradle plugin `io.micronaut.application` / `io.micronaut.library`, or Maven Micronaut plugin and Micronaut dependencies. | Generic Gradle/Maven and annotation processing are not unique to Micronaut; plugin may apply to a library module rather than an app. |
| Spring Boot | [Docs](https://docs.spring.io/spring-boot/reference/using/build-systems.html) | Boot dependencies/starters, parent/BOM or plugin plus Boot application bootstrap. | Generic `application.yml` does not prove Boot; neither Boot nor `bootstrap.yml` alone proves Spring Cloud. Shared BOMs do not make every module a Boot app. |
| Ktor | [Docs](https://ktor.io/docs/server-create-a-new-project.html) | Ktor server dependencies and server application/module source, corroborated by build configuration. | `io.ktor` client dependencies alone do not establish a Ktor server. |

## Python

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| Django | [Docs](https://docs.djangoproject.com/en/dev/intro/tutorial01/) | `django` declared in package/dependency manifest; `manage.py` and `settings.py` corroborate. | `manage.py` can be custom or generated/copied; Python manifests alone do not imply Django. |
| Flask | [Docs](https://flask.palletsprojects.com/en/stable/quickstart/) | `Flask` declared in project dependencies and source imports `from flask import Flask`; app/Wsgi entrypoint is corroborating only. | Flask imposes no standard project layout; `app.py` or `wsgi.py` alone is weak evidence. |
| Starlette | [Docs](https://www.starlette.io/) | Direct `starlette` dependency and source constructing a `Starlette` application. | FastAPI depends on Starlette; if FastAPI is declared, classify FastAPI as direct framework and Starlette as substrate unless used independently. |
| FastAPI | [Docs](https://fastapi.tiangolo.com/tutorial/first-steps/) | Direct `fastapi` dependency and a `FastAPI()` application with route registration. | Uvicorn and ASGI alone do not prove FastAPI; Starlette may be transitive. |

## PHP and Ruby

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| Laravel | [Docs](https://laravel.com/framework/docs/13.x/installation) | `artisan` plus Composer `laravel/framework` dependency; `bootstrap/app.php`, `routes/`, and Laravel directory conventions corroborate. | `artisan` can be copied/relocated; Laravel package dependencies can appear in packages/tests. Confirm app root. |
| WordPress | [Docs](https://developer.wordpress.org/advanced-administration/wordpress/wp-config/) | Core tree such as `wp-includes/`, `wp-admin/`, `wp-content/`; `wp-config.php` is additional evidence. | `wp-config.php` is generated at setup and may be absent, moved above root, or excluded because it contains DB credentials. `wp-content` may be a theme/plugin-only repository, not WordPress core. Never expose config values. |
| Ruby on Rails | [Docs](https://guides.rubyonrails.org/getting_started.html) | Gemfile declares `rails`; `config/application.rb`, `bin/rails`, `config/routes.rb` corroborate. | `Gemfile`, `Rakefile`, and `config/application.rb` separately are generic/custom signals; inspect gem dependency and root. |
| Hanami | [Docs](https://hanakai.org/learn/hanami/v2.3/getting-started) | Gemfile includes `hanami`; generated app also has `config/`, `app/`, `bin/hanami`, and `hanami new` conventions. | Ruby apps may use Hanami component gems independently; require the full framework gem/app structure before labeling it Hanami. |
| Symfony | [Docs](https://symfony.com/doc/current/setup.html) | Framework dependencies such as `symfony/framework-bundle` and an application kernel/config; console and lockfile corroborate. | Standalone Symfony components are also used by other frameworks; `bin/console` alone is not proof. |

## .NET

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| ASP.NET Core | [Docs](https://learn.microsoft.com/en-us/aspnet/core/razor-pages/web-sdk?view=aspnetcore-10.0) | Project SDK `Microsoft.NET.Sdk.Web` in app csproj or ASP.NET Core package/runtime references. | .NET Web SDK strongly supports ASP.NET Core but does not alone identify MVC, Razor Pages, API, Blazor, or other app style. |
| Blazor WebAssembly | [Docs](https://learn.microsoft.com/en-us/dotnet/architecture/blazor-for-web-forms-developers/project-structure) | csproj SDK `Microsoft.NET.Sdk.BlazorWebAssembly` and/or `Microsoft.AspNetCore.Components.WebAssembly`; `.razor` components corroborate. | Server-side Blazor uses `Microsoft.NET.Sdk.Web`, shared with non-Blazor ASP.NET; do not equate every web SDK project with Blazor. |

## Mobile and native

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| Android | [Docs](https://developer.android.com/build) | Per-module Gradle applies `com.android.application` or `com.android.library`; `android { }`, `src/main/AndroidManifest.xml`, Kotlin/Java sources corroborate. | Manifest can exist in libraries/fixtures; standalone `AndroidManifest.xml` does not prove Kotlin/Android build. In multi-module builds, scope it to the Gradle module. |
| Flutter | [Docs](https://docs.flutter.dev/tools/pubspec) | `pubspec.yaml` has `dependencies: flutter: sdk: flutter` (strong signal); Flutter app directories/platforms corroborate. | `pubspec.yaml` is present in all Dart packages, so filename alone only indicates Dart package ecosystem; Flutter may be an add-to-app module. |
| React Native | [Docs](https://reactnative.dev/docs/set-up-your-environment) | App manifest declares `react-native`; iOS/Android native projects and Metro entrypoint corroborate. | `react-native` can be transitive or a library dependency; Expo projects also use React Native, so distinguish Expo tooling/framework when its config/dependency exists. |
| Expo | [Docs](https://docs.expo.dev/get-started/create-a-project/) | App manifest declares `expo`; root `app.json`/`app.config.js`/`app.config.ts` and `expo start` scripts corroborate. | Expo modules/tooling can be dependencies of non-app packages; app config is the stronger root-level marker. Expo may generate native `android/`/`ios/` directories too. |
| SwiftUI / Apple application | [Docs](https://developer.apple.com/documentation/swiftui/app) | Target source imports SwiftUI and implements its App/View APIs; inspect Xcode/Swift target and platform settings. | `Package.swift` does not prove iOS or SwiftUI, and SwiftUI spans multiple Apple platforms. Do not infer UI framework from an Xcode project alone. |

## Elixir, Go and Rust

| Candidate | Official documentation | Positive evidence | Caveat |
| --- | --- | --- | --- |
| Phoenix (Elixir) | [Docs](https://phoenix.hexdocs.pm/directory_structure.html) | Mix app dependency `{:phoenix, ...}` in `mix.exs`; generated structure includes `lib/*_web/`, `config/`, `mix phx.server`. | Phoenix is commonly one app inside an umbrella; inspect each Mix app. Phoenix may be optional or excluded with API/minimal generator flags. |
| Gin (Go) | [Docs](https://gin-gonic.com/en/docs/quickstart/) | Relevant module `go.mod` requires `github.com/gin-gonic/gin`; Go source imports it and constructs `gin.Default()`/routes. | A module can list but not use a dependency; `go.mod` alone only establishes module/dependency metadata. |
| Echo (Go) | [Docs](https://echo.labstack.com/docs/quick-start) | Relevant `go.mod` includes `github.com/labstack/echo/v4` or `/v5`; Go source imports it and calls `echo.New()`. | Echo module version/path matters (v4/v5 coexist); a dependency may be unused or belong to a library/tool package. |
| Axum (Rust) | [Docs](https://docs.rs/axum/latest/axum/) | Project `Cargo.toml` dependency `axum`; source imports `axum::Router` / routing APIs; Tokio often accompanies it. | Cargo workspace may have several crate roots; Axum can be a library dependency and Tokio alone is not an Axum signal. |
| Actix Web (Rust) | [Docs](https://actix.rs/docs/getting-started) | Crate manifest has `actix-web`; source imports `actix_web::{App, HttpServer, ...}`. | Distinguish Actix Web from separate actor crate `actix`; Cargo.lock may contain transitive Actix crates without this project being an HTTP app. |

## Legacy and unlisted frameworks

For legacy Remix v2, check `@remix-run/*` packages, Remix Vite/build integration and
route source against the [Remix quick start](https://v2.remix.run/docs/start/quickstart/).
Do not relabel it React Router framework mode without migration evidence.

Unlisted frameworks are not unsupported: apply the same dependency/config/source
corroboration and consult official documentation. Record the specific evidence and
unknowns instead of inventing a generic match. Build tools (Vite, sbt, CMake),
runtimes, ORMs and application frameworks belong to separate categories.
