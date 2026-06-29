.. _us-012:

US-012 — Socle d'industrialisation et garanties de sécurité
===========================================================

:Statut: Spécifié
:Version cible: ``v0.1.0``
:Issue GitHub: ``[US-012]`` (à créer)
:Origine: cahier des charges ``baobab-auth-security v0.1.0`` (sections 1, 4, 9, 10)

Récit
-----

**En tant que** mainteneur de l'écosystème ``baobab-auth``,
**je veux** un package ``baobab_auth_security`` correctement initialisé, typé,
configurable et couvert par des tests de non-fuite de secret,
**afin de** livrer une librairie réutilisable, sûre et documentée.

Critères d'acceptation
----------------------

#. Le package ``baobab_auth_security`` existe en layout ``src/`` avec ``py.typed``,
   ``version.py`` et une hiérarchie d'exceptions dédiée.
#. La configuration est **injectée** via ``pydantic-settings`` ; aucune dépendance
   interdite (``fastapi``, ``sqlalchemy``, ``alembic``, ``psycopg``, ``asyncpg``,
   ``redis``, ``uvicorn``) n'est ajoutée en runtime obligatoire.
#. Des tests de sécurité garantissent l'**absence de fuite** de mot de passe brut,
   refresh token brut, access token complet et clé privée dans logs / exceptions /
   ``repr``.
#. ``ruff``, ``mypy``, ``pytest`` (couverture ≥ 95 %), ``build`` et ``twine check``
   passent ; la documentation MVP (README, CHANGELOG, ``integration_core``,
   ``security``) est à jour.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-012.1-initialisation-package
   FEAT-012.2-tests-securite-doc
