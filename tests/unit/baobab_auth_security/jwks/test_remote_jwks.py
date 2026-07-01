"""Tests du parsing JWKS distant.

:spec: FEAT-020.2
"""

from __future__ import annotations

from datetime import UTC, datetime

import httpx
import pytest

from baobab_auth_security.clock.fixed_clock import FixedClock
from baobab_auth_security.exceptions import JwksFetchError
from baobab_auth_security.jwks.jwk_public_key_loader import JwkPublicKeyLoader
from baobab_auth_security.jwks.jwks_document_parser import JwksDocumentParser
from baobab_auth_security.jwks.jwks_provider import LocalJwksProvider
from baobab_auth_security.jwks.public_jwk_converter import PublicJwkConverter
from baobab_auth_security.jwks.remote_jwks_fetcher import RemoteJwksFetcher
from baobab_auth_security.keys.ec_key_generator import EcKeyGenerator
from baobab_auth_security.keys.ed25519_key_generator import Ed25519KeyGenerator
from baobab_auth_security.keys.in_memory_key_provider import InMemoryKeyProvider
from baobab_auth_security.keys.key_generator import KeyGenerator

_NOW = datetime(2026, 6, 28, 12, 0, tzinfo=UTC)


def _rsa_jwks_document() -> dict[str, object]:
    pair = KeyGenerator(FixedClock(_NOW)).generate(kid="rsa-remote")
    return (
        LocalJwksProvider(InMemoryKeyProvider((pair,)), PublicJwkConverter())
        .jwks()
        .to_dict()
    )


class TestJwksDocumentParser:
    """Vérifie le round-trip local → JSON → clés publiques."""

    def test_FEAT_020_2_round_trip_rsa_jwks(self) -> None:
        document = _rsa_jwks_document()
        jwks, keys = JwksDocumentParser().parse(document)
        assert jwks.key_ids() == ("rsa-remote",)
        assert keys["rsa-remote"].key_size == 2048


class TestRemoteJwksFetcher:
    """Vérifie la récupération HTTP du JWKS."""

    def test_FEAT_020_2_fetches_jwks_over_http(self) -> None:
        document = _rsa_jwks_document()

        def handler(request: httpx.Request) -> httpx.Response:
            assert str(request.url) == "https://auth.example.com/auth/jwks"
            return httpx.Response(200, json=document)

        fetcher = RemoteJwksFetcher(
            "https://auth.example.com/auth/jwks",
            transport=httpx.MockTransport(handler),
        )
        jwks = fetcher.fetch()
        assert jwks.key_ids() == ("rsa-remote",)
        assert fetcher.public_key_for_kid("rsa-remote").key_size == 2048

    def test_FEAT_020_2_unknown_kid_raises(self) -> None:
        document = _rsa_jwks_document()

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=document)

        fetcher = RemoteJwksFetcher(
            "https://auth.example.com/jwks",
            transport=httpx.MockTransport(handler),
        )
        with pytest.raises(JwksFetchError):
            fetcher.public_key_for_kid("missing")

    def test_FEAT_020_2_round_trip_ec_and_okp(self) -> None:
        ec = EcKeyGenerator(FixedClock(_NOW)).generate(kid="ec-remote")
        ed = Ed25519KeyGenerator(FixedClock(_NOW)).generate(kid="ed-remote")
        document = LocalJwksProvider(
            InMemoryKeyProvider((ec, ed)), PublicJwkConverter()
        ).jwks().to_dict()
        jwks, keys = JwksDocumentParser().parse(document)
        assert set(jwks.key_ids()) == {"ec-remote", "ed-remote"}
        assert len(keys) == 2

    def test_FEAT_020_2_parser_rejects_invalid_document(self) -> None:
        with pytest.raises(JwksFetchError):
            JwksDocumentParser().parse({})
        with pytest.raises(JwksFetchError):
            JwksDocumentParser().parse({"keys": "bad"})

    def test_FEAT_020_2_loader_rejects_invalid_jwk(self) -> None:
        loader = JwkPublicKeyLoader()
        with pytest.raises(JwksFetchError):
            loader.load({"kty": "RSA"})
        with pytest.raises(JwksFetchError):
            loader.load({"kty": "UNKNOWN", "kid": "k", "alg": "RS256"})

    def test_FEAT_020_2_fetcher_rejects_empty_url(self) -> None:
        from baobab_auth_security.exceptions import ConfigurationError

        with pytest.raises(ConfigurationError):
            RemoteJwksFetcher("")

    def test_FEAT_020_2_jwks_lazy_load(self) -> None:
        document = _rsa_jwks_document()

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=document)

        fetcher = RemoteJwksFetcher(
            "https://auth.example.com/jwks",
            transport=httpx.MockTransport(handler),
        )
        assert fetcher.jwks().key_ids() == ("rsa-remote",)

    def test_FEAT_020_2_http_error_raises(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(503)

        fetcher = RemoteJwksFetcher(
            "https://auth.example.com/jwks",
            transport=httpx.MockTransport(handler),
        )
        with pytest.raises(JwksFetchError):
            fetcher.fetch()
