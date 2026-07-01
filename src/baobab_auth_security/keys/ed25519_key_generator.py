"""Génération de paires de clés Ed25519 (OKP).

:spec: FEAT-020.1
"""

from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric import ed25519

from baobab_auth_security.clock.clock import Clock
from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.keys.key_id_deriver import KeyIdDeriver
from baobab_auth_security.keys.key_pair import KeyPair
from baobab_auth_security.keys.key_status import KeyStatus


class Ed25519KeyGenerator:
    """Génère des paires de clés Ed25519 pour l'algorithme ``EdDSA``.

    :param clock: Horloge UTC injectée (date de création).
    """

    def __init__(self, clock: Clock) -> None:
        """Initialise le générateur."""
        self._clock = clock

    def generate(
        self,
        kid: str | None = None,
        status: KeyStatus = KeyStatus.ACTIVE,
    ) -> KeyPair:
        """Génère une paire de clés Ed25519.

        :param kid: Identifiant de clé ; dérivé de la clé publique si ``None``.
        :param status: Statut initial.
        :returns: La paire de clés générée.
        """
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        return KeyPair(
            kid=kid or KeyIdDeriver.derive(public_key),
            algorithm=KeyAlgorithm.EdDSA,
            private_key=private_key,
            public_key=public_key,
            status=status,
            created_at=self._clock.now(),
        )
