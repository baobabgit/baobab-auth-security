"""Récupération d'un JWKS distant via HTTP.

Nécessite l'extra ``remote-jwks`` (``httpx``).

:spec: FEAT-020.2
"""

from __future__ import annotations

from typing import Any, cast

from baobab_auth_security.exceptions import ConfigurationError, JwksFetchError
from baobab_auth_security.jwks.jwks import JWKS
from baobab_auth_security.jwks.jwks_document_parser import JwksDocumentParser
from baobab_auth_security.tokens.signing_key_types import SigningPublicKey


class RemoteJwksFetcher:
    """Télécharge et parse un JWKS depuis une URL HTTPS.

    :param url: URL du endpoint JWKS.
    :param timeout_seconds: Délai HTTP maximal.
    :param transport: Transport httpx injecté (tests) ; défaut client réel.
    :param parser: Parseur de document ; défaut :class:`JwksDocumentParser`.
    """

    def __init__(
        self,
        url: str,
        *,
        timeout_seconds: float = 10.0,
        transport: object | None = None,
        parser: JwksDocumentParser | None = None,
    ) -> None:
        """Initialise le fetcher."""
        if not url:
            raise ConfigurationError("URL JWKS vide.")
        self._url = url
        self._timeout = timeout_seconds
        self._transport = transport
        self._parser = parser or JwksDocumentParser()
        self._jwks: JWKS | None = None
        self._keys: dict[str, SigningPublicKey] | None = None

    @property
    def url(self) -> str:
        """URL configurée du JWKS distant.

        :returns: URL du endpoint.
        """
        return self._url

    def fetch(self) -> JWKS:
        """Télécharge et met en cache le JWKS distant.

        :returns: Document JWKS parsé.
        :raises JwksFetchError: Si la requête ou le parsing échoue.
        """
        document = self._download()
        jwks, keys = self._parser.parse(document)
        self._jwks = jwks
        self._keys = keys
        return jwks

    def jwks(self) -> JWKS:
        """Retourne le JWKS (télécharge si nécessaire).

        :returns: JWKS distant.
        """
        if self._jwks is None:
            return self.fetch()
        return self._jwks

    def public_key_for_kid(self, kid: str) -> SigningPublicKey:
        """Résout une clé publique par ``kid`` depuis le JWKS distant.

        :param kid: Identifiant de clé.
        :returns: Clé publique correspondante.
        :raises JwksFetchError: Si le ``kid`` est absent après fetch.
        """
        keys = self._keys
        if keys is None:
            self.fetch()
            keys = self._keys
        if keys is None:
            raise JwksFetchError("JWKS distant non chargé.")
        try:
            return keys[kid]
        except KeyError as exc:
            raise JwksFetchError(
                f"kid inconnu dans le JWKS distant : {kid!r}."
            ) from exc

    def _download(self) -> dict[str, object]:
        """Exécute la requête HTTP GET.

        :returns: Corps JSON décodé.
        :raises JwksFetchError: Si httpx est absent ou la requête échoue.
        """
        try:
            import httpx
        except ImportError as exc:
            raise JwksFetchError(
                "httpx requis pour le JWKS distant ; installez "
                "baobab-auth-security[remote-jwks]."
            ) from exc

        try:
            with httpx.Client(
                transport=cast(Any, self._transport), timeout=self._timeout
            ) as client:
                response = client.get(self._url)
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise JwksFetchError("Échec de récupération du JWKS distant.") from exc

        if not isinstance(payload, dict):
            raise JwksFetchError("Réponse JWKS invalide (JSON objet attendu).")
        return payload
