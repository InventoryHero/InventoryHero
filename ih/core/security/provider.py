from enum import Enum


class AuthenticationProvider(str, Enum):
    local = "local"
    oidc = "oidc"