"""Fournisseur de JWKS public local.

:spec: FEAT-010.4, ADR-0006
"""

from __future__ import annotations

from baobab_auth_security.jwks.jwks import JWKS
from baobab_auth_security.jwks.public_jwk_converter import PublicJwkConverter
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_status import KeyStatus

_PUBLISHED_STATUSES = frozenset({KeyStatus.ACTIVE, KeyStatus.RETIRED})


class LocalJwksProvider:
    """Construit un JWKS public à partir d'un fournisseur de clés local.

    Seules les clés ``ACTIVE`` et ``RETIRED`` sont publiées ; les clés
    ``PENDING`` sont omises. Le JWKS ne contient **aucune** clé privée.

    :param key_provider: Fournisseur de clés en mémoire.
    :param converter: Convertisseur public → JWK ; défaut
        :class:`PublicJwkConverter`.
    """

    def __init__(
        self,
        key_provider: InMemoryKeyProvider,
        converter: PublicJwkConverter | None = None,
    ) -> None:
        """Initialise le fournisseur de JWKS."""
        self._keys = key_provider
        self._converter = converter or PublicJwkConverter()

    def jwks(self) -> JWKS:
        """Retourne le JWKS public courant.

        :returns: Ensemble de JWK publiques (clés publiées uniquement).
        """
        jwk_list = tuple(
            self._converter.to_jwk(pair.public_key, pair.kid, pair.algorithm)
            for pair in self._keys.all_keys()
            if pair.status in _PUBLISHED_STATUSES
        )
        return JWKS(keys=jwk_list)
