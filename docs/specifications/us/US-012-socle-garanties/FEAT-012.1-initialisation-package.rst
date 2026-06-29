FEAT-012.1 — Initialisation du package
======================================

:Rattachée à: :ref:`us-012`
:Backlog: ``BL-S-010-001``
:Issue GitHub: ``[FEAT-012.1]`` (sub-issue de ``[US-012]``)
:Implémentation: :mod:`baobab_auth_security`

Description
-----------

Transformer le squelette template en package ``baobab_auth_security`` :
métadonnées ``pyproject.toml``, dépendance runtime ``baobab-auth-core``,
``py.typed``, ``version.py``, hiérarchie d'exceptions, horloge injectable
(``clock``).

Critères d'acceptation
----------------------

#. ``import baobab_auth_security`` expose ``__version__`` et un ``__all__`` stable.
#. ``pyproject.toml`` déclare ``baobab-auth-core >=0.4.0,<1.0.0`` en dépendance
   runtime et ``argon2-cffi``, ``cryptography``, ``PyJWT`` ; aucune dépendance
   interdite.
#. ``SecurityError`` est la racine de la hiérarchie d'exceptions du package.
#. ``Clock`` / ``SystemClock`` / ``FixedClock`` fournissent une horloge UTC
   injectable, compatible avec le port ``Clock`` du core.
#. ``make all`` passe sur le socle initial.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-012.1.1`` Adapter ``pyproject.toml`` et supprimer ``example_package``.
* ``TASK-012.1.2`` Créer ``version.py``, ``py.typed``, ``exceptions``.
* ``TASK-012.1.3`` Implémenter le module ``clock`` et ses tests.
