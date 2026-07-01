"""Chargement d'une clé publique depuis un document JWK JSON.

:spec: FEAT-020.2
"""

from __future__ import annotations

from typing import Any

from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa

from baobab_auth_security.exceptions import JwksFetchError
from baobab_auth_security.jwks.base64url_decoder import Base64UrlDecoder
from baobab_auth_security.jwks.ec_jwk import EcJwk
from baobab_auth_security.jwks.jwk import JWK
from baobab_auth_security.jwks.okp_jwk import OkpJwk
from baobab_auth_security.jwks.public_jwk import PublicJwk
from baobab_auth_security.tokens.signing_key_types import SigningPublicKey

_CURVE_BY_NAME: dict[str, ec.EllipticCurve] = {
    "P-256": ec.SECP256R1(),
    "P-384": ec.SECP384R1(),
    "P-521": ec.SECP521R1(),
}


class JwkPublicKeyLoader:
    """Reconstruit une clé publique et une JWK typée depuis un dict JSON."""

    def load(self, data: dict[str, Any]) -> tuple[PublicJwk, SigningPublicKey]:
        """Charge une entrée JWK.

        :param data: Dictionnaire JWK (champs publics uniquement).
        :returns: Paire JWK typée + clé publique cryptography.
        :raises JwksFetchError: Si le document est invalide ou non supporté.
        """
        kty = data.get("kty")
        kid = data.get("kid")
        alg = data.get("alg")
        if (
            not isinstance(kty, str)
            or not isinstance(kid, str)
            or not isinstance(alg, str)
        ):
            raise JwksFetchError("JWK invalide : kty, kid et alg sont requis.")

        if kty == "RSA":
            return self._load_rsa(data, kid, alg)
        if kty == "EC":
            return self._load_ec(data, kid, alg)
        if kty == "OKP":
            return self._load_okp(data, kid, alg)
        raise JwksFetchError(f"Type de clé JWKS non supporté : {kty!r}.")

    def _load_rsa(
        self, data: dict[str, Any], kid: str, alg: str
    ) -> tuple[JWK, rsa.RSAPublicKey]:
        n = data.get("n")
        e = data.get("e")
        if not isinstance(n, str) or not isinstance(e, str):
            raise JwksFetchError("JWK RSA invalide : n et e requis.")
        public_key = rsa.RSAPublicNumbers(
            e=Base64UrlDecoder.decode_uint(e),
            n=Base64UrlDecoder.decode_uint(n),
        ).public_key()
        jwk = JWK(kid=kid, alg=alg, n=n, e=e)
        return jwk, public_key

    def _load_ec(
        self, data: dict[str, Any], kid: str, alg: str
    ) -> tuple[EcJwk, ec.EllipticCurvePublicKey]:
        crv = data.get("crv")
        x = data.get("x")
        y = data.get("y")
        if not isinstance(crv, str) or not isinstance(x, str) or not isinstance(y, str):
            raise JwksFetchError("JWK EC invalide : crv, x et y requis.")
        curve = _CURVE_BY_NAME.get(crv)
        if curve is None:
            raise JwksFetchError(f"Courbe EC non supportée : {crv!r}.")
        public_key = ec.EllipticCurvePublicNumbers(
            x=Base64UrlDecoder.decode_uint(x),
            y=Base64UrlDecoder.decode_uint(y),
            curve=curve,
        ).public_key()
        jwk = EcJwk(kid=kid, alg=alg, crv=crv, x=x, y=y)
        return jwk, public_key

    def _load_okp(
        self, data: dict[str, Any], kid: str, alg: str
    ) -> tuple[OkpJwk, ed25519.Ed25519PublicKey]:
        crv = data.get("crv")
        x = data.get("x")
        if not isinstance(crv, str) or not isinstance(x, str):
            raise JwksFetchError("JWK OKP invalide : crv et x requis.")
        if crv != "Ed25519":
            raise JwksFetchError(f"Courbe OKP non supportée : {crv!r}.")
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(
            Base64UrlDecoder.decode_bytes(x)
        )
        jwk = OkpJwk(kid=kid, alg=alg, crv=crv, x=x)
        return jwk, public_key
