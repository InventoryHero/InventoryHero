from pydantic_settings import BaseSettings


class OidcSettings(BaseSettings):
    # TODO SERVICE ACCOUNT TOKENS FOR PERIODIC USER SYNC
    IH_OIDC_CONFIGURATION_URL: str | None = None
    IH_OIDC_CLIENT_ID: str | None = None
    IH_OIDC_CLIENT_SECRET: str | None = None
    IH_OIDC_REDIRECT_URI: str | None = None
    IH_OIDC_USER_CLAIM: str = "preferred_username"

    IH_OIDC_NAME: str = 'SSO'

    @property
    def enabled(self) -> bool:
        return all([
            self.IH_OIDC_CONFIGURATION_URL,
            self.IH_OIDC_CLIENT_ID,
            self.IH_OIDC_CLIENT_SECRET
        ])

    @property
    def user_claim(self) -> str:
        return self.IH_OIDC_USER_CLAIM.lower()