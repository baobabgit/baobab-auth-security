# Rapport de release — v0.1.0

Date : 2026-06-30  
Tag : v0.1.0

## Pré-release

- [x] Tous les backlogs v0.1.0 mergés sur `version/v0.1.0`
- [x] `uv run nox -s all` vert (couverture 100 %)
- [x] `CHANGELOG.md` section `[0.1.0]`
- [x] `pyproject.toml` version `0.1.0`
- [x] Correction `release.yml` (nom package PyPI)

## Artefacts

- [x] sdist (build local + CI)
- [x] wheel (build local + CI)
- [x] Release GitHub ([v0.1.0](https://github.com/baobabgit/baobab-auth-security/releases/tag/v0.1.0))
- [ ] PyPI — **échec 2026-07-01** : projet absent ; configurer *pending publisher*
  (voir `docs/workflow/SETUP.md` §6) puis relancer workflow Release.

## Diagnostic échec PyPI (run 28532178248)

```
400 Non-user identities cannot create new projects
```

Cause : pas de *pending publisher* PyPI pour `baobab-auth-security` avant le 1er upload.
Corrections : `release.yml` (artefacts wheel/sdist uniquement, `workflow_dispatch`).
