import urllib.parse

import requests
from django.conf import settings

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

SCOPE = "user-top-read user-library-read user-read-private"


def get_authorization_url():
    params = {
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "scope": SCOPE,
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "show_dialog": True,
    }

    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"


def get_access_token(code):
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
        "client_id": settings.SPOTIFY_CLIENT_ID,
        "client_secret": settings.SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()

    return response.json()


def get_user_profile(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers=headers,
    )

    response.raise_for_status()

    return response.json()