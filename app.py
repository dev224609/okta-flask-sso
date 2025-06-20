import os
from flask import Flask, session, redirect, url_for, render_template, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from urllib.parse import urlencode

# 1. Load environment variables
load_dotenv()
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
OKTA_ISSUER = os.getenv("OKTA_ISSUER")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# 2. Flask & OAuth setup
app = Flask(__name__, static_folder="static")
app.secret_key = FLASK_SECRET_KEY

oauth = OAuth(app)
oauth.register(
    name="okta",
    client_id=OKTA_CLIENT_ID,
    client_secret=OKTA_CLIENT_SECRET,
    server_metadata_url=f"{OKTA_ISSUER}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email"
    }
)

# 3. Home page
@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

# 4. Redirect to Okta for login
@app.route("/login")
def login():
    redirect_uri = url_for("auth_callback", _external=True)
    return oauth.okta.authorize_redirect(redirect_uri)

# 5. OAuth2 callback
@app.route("/callback")
def auth_callback():
    # Exchange code for tokens
    token = oauth.okta.authorize_access_token()
    # Pop the nonce that Authlib stored
    nonce = session.pop("oauth_okta_nonce", None)

    # Parse the ID Token claims
    userinfo = oauth.okta.parse_id_token(token, nonce=nonce)
    # Save both tokens & claims in session
    session["user"] = {
        "id_token": token.get("id_token"),
        "access_token": token.get("access_token"),
        "claims": userinfo
    }
    return redirect(url_for("profile"))

# 6. Profile page (requires auth)
@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("index"))
    return render_template("profile.html", user=user)

# 7. Logout (app + Okta)
@app.route("/logout")
def logout():
    user = session.pop("user", None)
    # Build Okta logout URL
    id_token = user.get("id_token") if user else ""

    # Grab a real OAuth2Session for "okta" and its metadata
    client = oauth.create_client("okta")
    client.load_server_metadata()
    end_session = client.server_metadata.get("end_session_endpoint")


    params = {
        "id_token_hint": id_token,
        "post_logout_redirect_uri": url_for("index", _external=True)
    }
    #logout_url = oauth.okta.client.server_metadata["end_session_endpoint"]
    #return redirect(oauth.okta.client.create_authorization_url(logout_url, **params)[0])

    logout_url = f"{end_session}?{urlencode(params)}"
    return redirect(logout_url)



if __name__ == "__main__":
    app.run(debug=True)