.. _us-010:

US-010 — Primitives cryptographiques de sécurité
================================================

:Statut: Spécifié
:Version cible: ``v0.1.0``
:Issue GitHub: ``[US-010]`` (à créer)
:Origine: cahier des charges ``baobab-auth-security v0.1.0`` (sections 4, 5, 6)

Récit
-----

**En tant qu'**\ intégrateur de l'écosystème ``baobab-auth``,
**je veux** disposer de primitives techniques de sécurité (hachage de mot de
passe, JWT signés localement, refresh tokens opaques, clés RSA et JWKS public),
**afin de** construire l'authentification d'une API sans réimplémenter la
cryptographie ni exposer de secret.

Critères d'acceptation
----------------------

#. Le hachage de mot de passe utilise **Argon2id** ; ``hash`` est non réversible
   et non vide, ``verify`` est sûr et retourne un booléen, ``needs_rehash``
   permet la migration des paramètres.
#. Les JWT sont signés localement en **RS256** par défaut, portent ``kid`` et
   ``alg`` dans le header et les claims requis (``sub``, ``jti``, ``sid``,
   ``roles``, ``permissions``, ``iat``, ``exp``, ``iss``, ``aud``).
#. La validation **refuse ``alg=none``** et tout algorithme non explicitement
   autorisé, et contrôle ``exp``/``iss``/``aud``.
#. Les refresh tokens sont **opaques, aléatoires**, rendus une seule fois en
   clair ; seul leur hash est destiné au stockage externe.
#. Les clés RSA sont générables, le **JWKS public ne contient aucune clé
   privée**, et toutes les dates manipulées sont **timezone-aware UTC**.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-010.1-hachage-argon2
   FEAT-010.2-jwt-rs256
   FEAT-010.3-refresh-tokens
   FEAT-010.4-cles-jwks
