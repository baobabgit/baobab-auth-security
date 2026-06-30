"""Configuration injectable de ``baobab-auth-security`` (pydantic-settings).

:spec: FEAT-012.2, ADR-0001
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from baobab_auth_security.keys.key_algorithm import KeyAlgorithm
from baobab_auth_security.password.password_hash_policy import PasswordHashPolicy
from baobab_auth_security.tokens.jwt_algorithm import JwtAlgorithm


class SecuritySettings(BaseSettings):
    """Paramètres de sécurité chargés depuis l'environnement.

    Préfixe d'environnement : ``BAOBAB_SECURITY_`` (ex.
    ``BAOBAB_SECURITY_ISSUER``). Aucun secret n'est stocké ici ; la configuration
    est **injectée** (aucun état global).

    :param issuer: Émetteur (``iss``) des tokens, ou ``None``.
    :param audience: Audience (``aud``) des tokens, ou ``None``.
    :param algorithm: Algorithme de signature JWT (``RS256`` par défaut).
    :param access_ttl_seconds: TTL des access tokens.
    :param refresh_ttl_seconds: TTL des refresh tokens.
    :param key_size: Taille des clés RSA générées, en bits.
    :param argon2_time_cost: Coût en temps d'Argon2.
    :param argon2_memory_cost: Coût mémoire d'Argon2, en KiB.
    :param argon2_parallelism: Parallélisme d'Argon2.
    """

    model_config = SettingsConfigDict(
        env_prefix="BAOBAB_SECURITY_",
        frozen=True,
        extra="ignore",
    )

    issuer: str | None = None
    audience: str | None = None
    algorithm: str = "RS256"
    access_ttl_seconds: int = Field(default=900, gt=0)
    refresh_ttl_seconds: int = Field(default=1_209_600, gt=0)
    key_size: int = Field(default=2048, ge=2048)
    argon2_time_cost: int = Field(default=3, ge=1)
    argon2_memory_cost: int = Field(default=65_536, ge=8)
    argon2_parallelism: int = Field(default=4, ge=1)

    def jwt_algorithm(self) -> JwtAlgorithm:
        """Résout l'algorithme JWT configuré.

        :returns: L'algorithme de signature.
        :raises InvalidAlgorithmError: Si l'algorithme n'est pas autorisé.
        """
        return JwtAlgorithm.from_name(self.algorithm)

    def key_algorithm(self) -> KeyAlgorithm:
        """Résout l'algorithme de clé configuré.

        :returns: L'algorithme de clé.
        :raises ConfigurationError: Si l'algorithme est inconnu.
        """
        return KeyAlgorithm.from_name(self.algorithm)

    def password_policy(self) -> PasswordHashPolicy:
        """Construit la politique Argon2 depuis la configuration.

        :returns: La politique de hachage correspondante.
        """
        return PasswordHashPolicy(
            time_cost=self.argon2_time_cost,
            memory_cost=self.argon2_memory_cost,
            parallelism=self.argon2_parallelism,
        )
