# Rapport d'intégration — baobab-auth-security v0.1.1 × baobab-auth-api v0.1.0

Date : 2026-07-01  
Producteur : baobab-auth-security  
Consommateur : baobab-auth-api (PyPI `v0.1.0`, branche `main`)  
Résultat : **PASSED**

## Périmètre validé

- `CorePasswordHasherAdapter`, `CoreTokenProviderAdapter`
- `LocalJwksProvider`, JWT RS256
- Émission et validation access/refresh tokens
- Exposition JWKS sans clé privée (`GET /.well-known/jwks.json`)

## Qualité consommateur

- Tests API login/refresh/me + JWKS : **PASSED**
- Dépendance : `baobab-auth-security>=0.1.1,<0.2.0` (PyPI `v0.1.1`)

## Référence

Rapport consommateur : `baobab-auth-api` —
`docs/integrations/reports/baobab-auth-security-v0.1.1__baobab-auth-api-v0.1.0.md`
