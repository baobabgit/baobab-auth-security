"""Types de clés asymétriques supportées pour JWT et JWKS.

:spec: FEAT-020.1
"""

from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePrivateKey,
    EllipticCurvePublicKey,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

type SigningPrivateKey = RSAPrivateKey | EllipticCurvePrivateKey | Ed25519PrivateKey
"""Clé privée utilisable pour signer un JWT."""

type SigningPublicKey = RSAPublicKey | EllipticCurvePublicKey | Ed25519PublicKey
"""Clé publique utilisable pour vérifier un JWT."""
