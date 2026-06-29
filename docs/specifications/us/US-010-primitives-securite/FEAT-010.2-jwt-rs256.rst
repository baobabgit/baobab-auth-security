FEAT-010.2 — JWT local signé en RS256
=====================================

:Rattachée à: :ref:`us-010`
:Backlog: ``BL-S-010-003``
:Issue GitHub: ``[FEAT-010.2]`` (sub-issue de ``[US-010]``)
:Implémentation: :class:`baobab_auth_security.tokens.jwt_token_provider.JwtTokenProvider`

Description
-----------

Encoder, décoder et valider des JSON Web Tokens signés localement en **RS256**
par défaut (via ``PyJWT``), avec ``kid`` dans le header, claims structurés et
contrôles de sécurité stricts.

Critères d'acceptation
----------------------

#. ``JwtEncoder`` produit un JWT compact signé RS256, header portant ``kid`` et
   ``alg``, claims ``sub``/``jti``/``sid``/``roles``/``permissions``/``iat``/
   ``exp``/``iss``/``aud`` selon configuration.
#. ``JwtDecoder`` vérifie la signature avec la clé publique correspondant au
   ``kid`` et reconstruit :class:`SecurityTokenClaims`.
#. ``JwtValidator`` **refuse ``alg=none``** et tout algorithme hors liste
   autorisée, et rejette un token expiré / d'``iss`` ou ``aud`` incohérent.
#. Un token altéré ou signé par une autre clé est rejeté par une exception
   dédiée sans fuite du secret.
#. Toutes les dates (``iat``, ``exp``) sont **UTC aware**.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-010.2.1`` Implémenter ``SecurityTokenClaims`` et ``SecurityTokenPair``.
* ``TASK-010.2.2`` Implémenter ``JwtEncoder`` / ``JwtDecoder`` / ``JwtValidator``.
* ``TASK-010.2.3`` Implémenter ``JwtTokenProvider`` et tester (positif/négatif).
