# Gate d'intégration aval — v0.1.0

Date : 2026-06-30  
Décision : **attendre** la validation `baobab-auth-core v0.5.1` par les
consommateurs restants avant de lancer l'intégration `baobab-auth-api` ×
`baobab-auth-security`.

## Contexte

La ref `version/v0.1.0` est **proposée** (`INTEGRATION_PENDING`) mais
l'intégration active côté `baobab-auth-api` est **différée** volontairement.

## État chaîne core v0.5.1

| Ordre | Consommateur | Statut core |
|-------|--------------|-------------|
| 1 | baobab-auth-database | **PASSED** |
| 2 | baobab-auth-security | **PASSED** |
| 3 | baobab-auth-api | **PENDING** |
| 4 | baobab-auth-client | **PENDING** |
| 5 | baobab-auth-admin | **PENDING** |

Source : `baobab-auth-core` —
`docs/integrations/compatibility_matrix.yaml`

## Condition de levée du gate

Démarrer l'intégration `baobab-auth-api` × `baobab-auth-security` lorsque les
ordres **3, 4 et 5** sont `PASSED` dans la matrice core (jalon
`INTEGRATION_VALIDATED` côté core).

## Action consommateur (quand le gate est levé)

```bash
uv add "baobab-auth-security @ git+https://github.com/baobabgit/baobab-auth-security.git@version/v0.1.0"
```

Puis reporter le résultat dans
`baobab-auth-security/docs/integrations/compatibility_matrix.yaml`.
