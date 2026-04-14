import os
from flask_appbuilder.security.manager import AUTH_OAUTH
from airflow.providers.fab.auth_manager.security_manager.override import FabAirflowSecurityManagerOverride
from flask import current_app

# ----------------------------------------------------
# Basic Security
# ----------------------------------------------------
CSRF_ENABLED = True

# ----------------------------------------------------
# Authentication
# ----------------------------------------------------
AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Viewer"

# ----------------------------------------------------
# OAuth Providers
# ----------------------------------------------------
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise RuntimeError("Google OAuth credentials are not set")

OAUTH_PROVIDERS = [
    {
        "name": "google",
        "icon": "fa-google",
        "token_key": "access_token",
        "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
        "remote_app": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
            "api_base_url": "https://openidconnect.googleapis.com/v1/",
            "client_kwargs": {
                "scope": "openid email profile"
            },
        },
    }
]

# ----------------------------------------------------
# Optional: restrict allowed domains
# ----------------------------------------------------
class CustomSecurityManager(FabAirflowSecurityManagerOverride):

    def auth_user_oauth(self, userinfo):
        email = userinfo.get("email")

        if email:
            user = self.find_user(email=email)
            if user:
                return user

        return super().auth_user_oauth(userinfo)


SECURITY_MANAGER_CLASS = CustomSecurityManager