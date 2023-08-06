import base64
import hashlib
import os
import webbrowser
from multiprocessing import Queue

import requests
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from oqtant.settings import Settings
from oqtant.util.server import ThreadServer

settings = Settings()

app = FastAPI(title="Login API", openapi_url="/openapi.json")
router = APIRouter()


def generate_random(length: int) -> str:
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8").replace("=", "")


verifier = generate_random(80)


def generate_challenge(verifier: str) -> str:
    hashed = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(hashed).decode("utf-8").replace("=", "")


def get_authentication_url():
    code_challenge = generate_challenge(verifier)
    auth_url = "".join(
        [
            f"{settings.auth0_base_url}/authorize",
            "?response_type=code",
            f"&scope={settings.auth0_scope}",
            f"&audience={settings.auth0_audience}",
            f"&code_challenge={code_challenge}",
            "&code_challenge_method=S256",
            f"&client_id={settings.auth0_client_id}",
            "&redirect_uri=http://localhost:8080",
        ]
    )
    return auth_url


queue = Queue()


@app.get("/")
async def main(code):
    resp = await get_token(verifier, code)
    token = resp["access_token"]
    queue.put({"token": token})
    if token:
        return "Successfully authenticated, you may close this tab now"
    else:
        return "Failed to authenticate, please close this tab and try again"


@app.get("/login")
def login():
    return RedirectResponse(url=get_authentication_url())


async def get_token(verifier: str, code: str):
    url = f"{settings.auth0_base_url}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.auth0_client_id,
        "code_verifier": verifier,
        "code": code,
        "redirect_uri": "http://localhost:8080",
    }
    resp = requests.post(
        url, headers=headers, data=data, allow_redirects=False, timeout=(5, 30)
    )
    return resp.json()


def get_user_token() -> str:
    """A utility function required for getting Oqtant authenticated with your Oqtant account.
       Starts up a server to handle the Auth0 authentication process and acquire a token.
    Returns:
        str: Auth0 user token
    """
    server_config = uvicorn.Config(
        app=app, host="localhost", port=8080, log_level="error"
    )
    server = ThreadServer(config=server_config)
    with server.run_in_thread():
        webbrowser.open("http://localhost:8080/login")
        token = queue.get(block=True)
    return token["token"]
