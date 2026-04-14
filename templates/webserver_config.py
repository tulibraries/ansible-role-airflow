import os
from flask_appbuilder.security.manager import AUTH_OAUTH

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
        "remote_app": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
            "client_kwargs": {
                "scope": "openid email profile"
            },
        },
    }
]

# ----------------------------------------------------
# Optional: restrict allowed domains
# ----------------------------------------------------
def oauth_user_info(provider, response=None):
    if provider == "google":
        email = response.get("email")

        if not email or not email.endswith("@temple.edu"):
            return None

        return {
            "username": email,
            "email": email,
            "first_name": response.get("given_name", ""),
            "last_name": response.get("family_name", ""),
        }
