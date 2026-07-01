FEAT-012.2 — Tests de non-fuite et documentation MVP
====================================================

:Rattachée à: :ref:`us-012`
:Backlog: ``BL-S-010-007``
:Issue GitHub: ``[FEAT-012.2]`` (sub-issue de ``[US-012]``)
:Implémentation: ``tests/security/`` et ``docs/``

Description
-----------

Couvrir les règles transverses de sécurité par des tests dédiés, fournir la
configuration injectable (``SecuritySettings``), des aides de test
déterministes, et la documentation MVP.

Critères d'acceptation
----------------------

#. ``tests/security/test_no_secret_leakage.py`` vérifie qu'aucun mot de passe
   brut, refresh token brut, access token complet ni clé privée n'apparaît dans
   ``repr`` / ``str`` / message d'exception.
#. ``SecuritySettings`` (``pydantic-settings``) centralise issuer, audience, TTLs,
   algorithme et paramètres Argon2, et se charge depuis l'environnement.
#. Un module ``testing`` expose une horloge fixe et un fournisseur de clés en
   mémoire pour des tests déterministes côté consommateurs.
#. ``README.md``, ``CHANGELOG.md``, ``docs/integration_core.md`` et
   ``docs/security.md`` sont à jour, ainsi que la matrice de compatibilité.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-012.2.1`` Implémenter ``SecuritySettings`` et le module ``testing``.
* ``TASK-012.2.2`` Écrire ``tests/security/test_no_secret_leakage.py``.
* ``TASK-012.2.3`` Rédiger la documentation MVP et la matrice de compatibilité.
