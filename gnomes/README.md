# gnomes/ — project gnome directory (stub)

Gnome directories for gnomes **homed in this repo** live here, one directory
per gnome (`gnomes/<gn_name>/` with `gnome.yml`, `prompt.md`, `fixtures/`).

Before creating one, follow the reuse protocol in the control repo
(`platform/docs/gnome-reuse.md`): search the central registry
(`platform/gnomes.yml`), prefer reuse or parameterization, and remember the
rubric — a deterministic task is code, not a gnome. Every gnome, wherever it
lives, is registered centrally in the control repo's `gnomes.yml`; spec and
creation procedure: `platform/docs/gnome-spec.md`.

Most projects start with zero homed gnomes: platform-homed gnomes can be
*deployed* to this repo (their `deployments:` list) without any files here.
