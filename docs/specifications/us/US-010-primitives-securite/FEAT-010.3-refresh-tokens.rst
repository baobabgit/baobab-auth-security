FEAT-010.3 — Refresh tokens opaques
===================================

:Rattachée à: :ref:`us-010`
:Backlog: ``BL-S-010-004``
:Issue GitHub: ``[FEAT-010.3]`` (sub-issue de ``[US-010]``)
:Implémentation: :class:`baobab_auth_security.refresh_tokens.refresh_token_generator.RefreshTokenGenerator`

Description
-----------

Générer des refresh tokens **opaques** (aléatoire cryptographique), leur hash
stockable et leur identifiant, avec dates d'émission et d'expiration UTC. Le
token en clair n'est exposé qu'une seule fois.

Critères d'acceptation
----------------------

#. ``RefreshTokenGenerator.generate()`` retourne un :class:`RefreshTokenResult`
   contenant un token opaque à forte entropie (``secrets``), son ``token_id``
   (``jti``), son hash et les dates ``issued_at`` / ``expires_at`` UTC aware.
#. ``RefreshTokenHasher.hash()`` produit un hash déterministe (SHA-256) du token,
   et ``verify()`` compare en temps constant.
#. Le token en clair est masqué dans ``repr`` / ``str`` du résultat ; seul le
   hash est destiné à la persistance externe (jamais persisté par security).
#. Deux générations successives produisent des tokens distincts.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-010.3.1`` Implémenter ``RefreshTokenHasher`` et ``RefreshTokenResult``.
* ``TASK-010.3.2`` Implémenter ``RefreshTokenGenerator`` et tester l'entropie/hash.
