from django.http import HttpResponse
from django.shortcuts import redirect, render

from .services import spotify


def index(request):
    return render(request, "library/index.html")


def login(request):
    authorization_url = spotify.get_authorization_url()

    return redirect(authorization_url)


def callback(request):
    if "error" in request.GET:
        return HttpResponse(
            f"Spotify authorization failed: {request.GET['error']}"
        )

    code = request.GET.get("code")

    if not code:
        return HttpResponse("No authorization code received.")

    token_info = spotify.get_access_token(code)

    request.session["access_token"] = token_info.get("access_token")
    request.session["refresh_token"] = token_info.get("refresh_token")

    return redirect("index")
