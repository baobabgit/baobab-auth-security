FEAT-010.1 — Hachage de mot de passe Argon2id
=============================================

:Rattachée à: :ref:`us-010`
:Backlog: ``BL-S-010-002``
:Issue GitHub: ``[FEAT-010.1]`` (sub-issue de ``[US-010]``)
:Implémentation: :class:`baobab_auth_security.password.argon2_password_hasher.Argon2PasswordHasher`

Description
-----------

Fournir un service de hachage de mot de passe fondé sur **Argon2id** (via
``argon2-cffi``), exposant un résultat typé masquant le hash dans ses
représentations, ainsi que la détection du besoin de re-hachage après évolution
des paramètres.

Critères d'acceptation
----------------------

#. ``hash(plain)`` retourne un :class:`PasswordHashResult` dont la valeur est non
   vide, non réversible et préfixée ``$argon2id$``.
#. ``verify(plain, hash)`` retourne un :class:`PasswordVerificationResult`
   (``is_valid`` booléen) en s'appuyant sur l'API constant-time d'Argon2.
#. ``verify`` sur un mauvais mot de passe retourne ``is_valid=False`` sans lever.
#. ``needs_rehash(hash)`` retourne ``True`` lorsque les paramètres de
   :class:`PasswordHashPolicy` ont changé.
#. Ni ``repr`` ni ``str`` du mot de passe en clair ou du résultat n'exposent le
   secret.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-010.1.1`` Implémenter ``PasswordHashPolicy`` et les résultats typés.
* ``TASK-010.1.2`` Implémenter ``Argon2PasswordHasher`` (hash/verify/needs_rehash).
* ``TASK-010.1.3`` Couvrir par tests positifs et négatifs (≥ 95 %).
