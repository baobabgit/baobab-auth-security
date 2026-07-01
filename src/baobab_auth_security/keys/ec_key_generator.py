"""Génération de paires de clés elliptiques (EC).

:spec: FEAT-020.1
"""

from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric import ec

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.exceptions import ConfigurationError
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_id_deriver import KeyIdDeriver
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.key_status import KeyStatus

_CURVE_BY_ALGORITHM: dict[KeyAlgorithm, ec.EllipticCurve] = {
    KeyAlgorithm.ES256: ec.SECP256R1(),
    KeyAlgorithm.ES384: ec.SECP384R1(),
    KeyAlgorithm.ES512: ec.SECP521R1(),
}


class EcKeyGenerator:
    """Génère des paires de clés EC pour ES256/ES384/ES512.

    :param clock: Horloge UTC injectée (date de création).
    """

    def __init__(self, clock: Clock) -> None:
        """Initialise le générateur."""
        self._clock = clock

    def generate(
        self,
        algorithm: KeyAlgorithm = KeyAlgorithm.ES256,
        kid: str | None = None,
        status: KeyStatus = KeyStatus.ACTIVE,
    ) -> KeyPair:
        """Génère une paire de clés EC.

        :param algorithm: Algorithme ES* associé.
        :param kid: Identifiant de clé ; dérivé de la clé publique si ``None``.
        :param status: Statut initial.
        :returns: La paire de clés générée.
        :raises ConfigurationError: Si l'algorithme n'est pas ES*.
        """
        curve = _CURVE_BY_ALGORITHM.get(algorithm)
        if curve is None:
            raise ConfigurationError(
                f"Algorithme EC non supporté pour la génération : {algorithm.value!r}."
            )
        private_key = ec.generate_private_key(curve)
        public_key = private_key.public_key()
        return KeyPair(
            kid=kid or KeyIdDeriver.derive(public_key),
            algorithm=algorithm,
            private_key=private_key,
            public_key=public_key,
            status=status,
            created_at=self._clock.now(),
        )
