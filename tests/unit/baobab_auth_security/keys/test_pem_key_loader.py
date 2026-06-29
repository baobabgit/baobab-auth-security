"""Tests de :class:`PemKeyLoader`.

:spec: FEAT-010.4
"""

from __future__ import annotations

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from baobab_auth_security.exceptions import KeyManagementError
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.pem_key_loader import PemKeyLoader


def _private_pem(key: RSAPrivateKey) -> bytes:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def _public_pem(key: RSAPublicKey) -> str:
    return key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


class TestPemKeyLoader:
    """Vérifie le chargement de clés RSA depuis du PEM."""

    def test_FEAT_010_4_round_trip_private_key(self, active_key: KeyPair) -> None:
        loader = PemKeyLoader()
        loaded = loader.load_private_key(_private_pem(active_key.private_key))
        assert isinstance(loaded, RSAPrivateKey)
        assert loaded.key_size == active_key.private_key.key_size

    def test_FEAT_010_4_round_trip_public_key(self, active_key: KeyPair) -> None:
        loader = PemKeyLoader()
        loaded = loader.load_public_key(_public_pem(active_key.public_key))
        assert isinstance(loaded, RSAPublicKey)

    def test_FEAT_010_4_invalid_private_pem_raises(self) -> None:
        with pytest.raises(KeyManagementError):
            PemKeyLoader().load_private_key("not a pem")

    def test_FEAT_010_4_invalid_public_pem_raises(self) -> None:
        with pytest.raises(KeyManagementError):
            PemKeyLoader().load_public_key("not a pem")

    def test_FEAT_010_4_rejects_non_rsa_private_key(self) -> None:
        ec_key = ec.generate_private_key(ec.SECP256R1())
        pem = ec_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with pytest.raises(KeyManagementError):
            PemKeyLoader().load_private_key(pem)

    def test_FEAT_010_4_rejects_non_rsa_public_key(self) -> None:
        ec_key = ec.generate_private_key(ec.SECP256R1())
        pem = ec_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with pytest.raises(KeyManagementError):
            PemKeyLoader().load_public_key(pem)
