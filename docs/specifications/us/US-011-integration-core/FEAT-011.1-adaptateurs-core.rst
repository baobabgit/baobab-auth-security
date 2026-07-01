FEAT-011.1 — Adaptateurs et mappers ``baobab-auth-core``
=======================================================

:Rattachée à: :ref:`us-011`
:Backlog: ``BL-S-010-006``
:Issue GitHub: ``[FEAT-011.1]`` (sub-issue de ``[US-011]``)
:Implémentation: :mod:`baobab_auth_security.integration`

Description
-----------

Brancher les services techniques riches de ``baobab-auth-security`` sur les ports
**réels** de ``baobab-auth-core >= 0.4.0`` via des adaptateurs stricts et des
mappers de value objects, et fournir un ``InMemoryRevocationChecker`` minimal par
``jti``.

Critères d'acceptation
----------------------

#. ``CorePasswordHasherAdapter`` enveloppe ``Argon2PasswordHasher`` et expose
   ``hash(PlainPassword) -> PasswordHash`` et ``verify(PlainPassword,
   PasswordHash) -> bool``.
#. ``CoreTokenProviderAdapter`` enveloppe ``JwtTokenProvider``, le générateur de
   refresh tokens et la révocation, et expose les six méthodes du port réel.
#. ``CoreClaimsMapper`` convertit ``SecurityTokenClaims`` ⇆ ``TokenClaims`` du core
   (et le ``dict`` décodé) sans recalculer rôle → permissions.
#. ``CoreTokenPairMapper`` convertit ``SecurityTokenPair`` → ``TokenPair`` du core.
#. ``InMemoryRevocationChecker`` révoque et teste un ``jti`` ; l'adaptateur de
   révocation refuse un access token dont le ``jti`` est révoqué.
#. Des tests d'intégration vérifient la conformité aux ``Protocol`` du core
   (``isinstance`` runtime-checkable) et les allers-retours de mapping.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-011.1.1`` Implémenter ``InMemoryRevocationChecker``.
* ``TASK-011.1.2`` Implémenter les adaptateurs ``CorePasswordHasherAdapter`` /
  ``CoreTokenProviderAdapter``.
* ``TASK-011.1.3`` Implémenter ``CoreClaimsMapper`` / ``CoreTokenPairMapper``.
* ``TASK-011.1.4`` Tests d'intégration contractuels contre ``baobab-auth-core``.
