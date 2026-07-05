# CLAUDE.md — kdc

KDC — agentic data center mapper: tracks US data center projects (announcements, permits, construction) as an open, source-transparent dataset with a browsable site.

This is a project repo of the **Bussetech Software Studio** — an agentic system that
manages a GitHub org, its repos, and their web presence with minimal human
touch. The studio's control repo is `bussetech/platform`; its front door is the
portal at `https://bussetech.com`. This repo publishes a static site to
`https://kdc.bussetech.com`.

> Founding note: this file was created from the studio's project template.
> The founding PR replaces this preamble with project-specific guidance
> (data model, sources, jobs); the studio sections below should survive.

## How this repo works

- **Site:** Jekyll + the shared studio theme, pinned by tag in `_config.yml`
  (`remote_theme:`). Never pin to a branch; bump versions canary-first
  (theme repo `docs/versioning.md`). Design rules: theme `docs/design.md` —
  Swiss typography, color is wayfinding only.
- **Data:** text-based stores in `data/`, one JSON Schema per dataset in
  `schema/` (`schema/<name>.schema.json` ↔ `data/<name>.*` — the studio
  data CI validates the pair). Published datasets are CC BY 4.0 and must
  state provenance in `data/index.md`.
- **Feed:** the theme publishes `/feed.json` (JSON Feed 1.1) from `_posts/`.
  The portal aggregates it — writing a post is how this project surfaces on
  the studio homepage.
- **Visibility:** `public` (declared in the control repo's
  `platform.yml`, the single source of truth). All machinery keys off that
  entry — do not contradict it here. For `private-published`: the site is
  public while the repo stays private; never emit repo URLs or source maps
  into the built site (the theme enforces this off `studio.visibility`).
- **CI:** `.github/workflows/ci.yml` calls the studio's shared reusable
  workflows (`bussetech/ci@v1` — site build/link/leak checks + data schema
  validation). `deploy.yml` builds and publishes to GitHub Pages, then pings
  the portal (`repository_dispatch: studio-content-updated` on `bussetech/www`)
  so it re-aggregates promptly.
- **Gnomes** (studio agents): check the central registry
  (`platform/gnomes.yml`) and the reuse protocol (`platform/docs/gnome-reuse.md`)
  before building anything agentic here. Gnome dirs homed in this repo live
  under `gnomes/`. Deterministic work is code, not a gnome.

## Working rules

- Conventional commits (`feat:`, `fix:`, `docs:`, …), atomic.
- Once the site is live, changes go through PRs; gnome/bot changes are
  always PRs — humans merge.
- Decisions a human must make become orange `needs-human` issues (with a
  recommendation and a default action). Status flows through the site feed
  and the portal, never through issues.
- Don't hardcode org/domain/branding beyond what the factory stamped into
  `_config.yml` — if those facts change, the studio re-stamps them.

## Detach procedure (if this repo leaves the studio)

This repo must keep working without the studio; its only bindings are:

1. **Registry entry** in `bussetech/platform` `platform.yml` — gone means the
   studio stops managing DNS/portal/UAT for it. Nothing in this repo breaks.
2. **Shared CI callers** (`ci.yml`): both jobs are guarded by
   `if: github.repository_owner == 'bussetech'` and skip green outside the
   org. To keep real CI after detaching, replace them with a plain
   `jekyll build` job (and any schema validation you want to keep).
3. **Deploy workflow** (`deploy.yml`): same owner guard. After detaching,
   remove the guard, drop the `ping-portal` job (the dispatch secrets and
   target are studio-specific), and wire GitHub Pages (or any static host)
   for the new home. The custom domain `kdc.bussetech.com` is
   studio DNS and does not travel.
4. **Theme**: `remote_theme: bussetech/theme@<tag>` is a public repo — it
   keeps working detached. To cut the last tie, vendor the theme or switch
   to any Jekyll theme.

Local build never needs studio access: `bundle install && bundle exec
jekyll serve`.
