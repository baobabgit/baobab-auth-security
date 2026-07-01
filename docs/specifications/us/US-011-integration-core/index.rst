.. _us-011:

US-011 — Intégration avec ``baobab-auth-core``
==============================================

:Statut: Spécifié
:Version cible: ``v0.1.0``
:Issue GitHub: ``[US-011]`` (à créer)
:Origine: cahier des charges ``baobab-auth-security v0.1.0`` (sections 3, 7)

Récit
-----

**En tant que** brique ``baobab-auth-core``,
**je veux** que ``baobab-auth-security`` expose des adaptateurs respectant
strictement mes ports ``PasswordHasher`` et ``TokenProvider`` et mappant les
value objects (``TokenClaims``, ``TokenPair``),
**afin de** déléguer la cryptographie sans dépendre d'une implémentation
concrète ni dupliquer mes value objects.

Critères d'acceptation
----------------------

#. ``CorePasswordHasherAdapter`` satisfait le ``Protocol`` réel
   ``baobab_auth_core.ports.password_hasher.PasswordHasher`` (méthodes ``hash``
   et ``verify``, **synchrones**).
#. ``CoreTokenProviderAdapter`` satisfait le ``Protocol`` réel
   ``baobab_auth_core.ports.token_provider.TokenProvider`` (``generate_token_id``,
   ``create_access_token``, ``verify_access_token`` → ``dict``,
   ``create_refresh_token``, ``verify_refresh_token`` → ``dict``, ``revoke_token``).
#. ``CoreClaimsMapper`` et ``CoreTokenPairMapper`` produisent les VO réels du core
   (``TokenClaims``, ``TokenPair``) sans recalculer le mapping rôle → permissions.
#. Les dates restent **UTC aware** ; aucun secret n'est exposé.
#. Tout écart entre les ports idéalisés du cahier (async, ``issue_token_pair``) et
   les ports réels du core est documenté (voir :doc:`ADR-0005 </architecture/adr/index>`).

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-011.1-adaptateurs-core
