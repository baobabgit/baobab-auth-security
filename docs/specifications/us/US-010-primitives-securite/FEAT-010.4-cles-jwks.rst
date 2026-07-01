FEAT-010.4 — Clés RSA et JWKS public local
==========================================

:Rattachée à: :ref:`us-010`
:Backlog: ``BL-S-010-005``
:Issue GitHub: ``[FEAT-010.4]`` (sub-issue de ``[US-010]``)
:Implémentation: :class:`baobab_auth_security.jwks.jwks_provider.LocalJwksProvider`

Description
-----------

Générer des paires de clés RSA (RS256/RS384/RS512), gérer leur cycle de vie en
mémoire et exposer un **JWKS public** ne contenant **aucune** clé privée.

Critères d'acceptation
----------------------

#. ``KeyGenerator.generate()`` produit une :class:`KeyPair` RSA ≥ 2048 bits avec
   un ``kid`` stable, un :class:`KeyAlgorithm` et un :class:`KeyStatus`.
#. ``InMemoryKeyProvider`` fournit la clé active de signature et la résolution
   par ``kid`` pour la vérification.
#. ``LocalJwksProvider.jwks()`` retourne un :class:`JWKS` dont chaque
   :class:`JWK` ne contient que les champs publics (``kty``, ``use``, ``alg``,
   ``kid``, ``n``, ``e``) — jamais ``d``, ``p``, ``q``.
#. La clé privée n'apparaît dans aucun ``repr`` / ``str`` / exception / JWKS.
#. Un chargeur PEM permet d'injecter des clés existantes.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-010.4.1`` Implémenter ``KeyAlgorithm``, ``KeyStatus``, ``KeyPair``.
* ``TASK-010.4.2`` Implémenter ``KeyGenerator``, ``InMemoryKeyProvider``, loader PEM.
* ``TASK-010.4.3`` Implémenter ``JWK``/``JWKS``/``LocalJwksProvider`` + conversion RSA.
