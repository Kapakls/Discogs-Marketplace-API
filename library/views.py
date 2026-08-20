import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from library.services.discogs.discogs import DiscogsService
from library.services.music.music import MusicService

from .models import Album, User
from .services.spotify.factory import create_spotify_service


def index(request):
    return render(request, "library/index.html")


def login(request):
    spotify = create_spotify_service()

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

    spotify = create_spotify_service()

    token = asyncio.run(
        spotify.exchange_code(code)
    )

    request.session["access_token"] = token.access_token
    request.session["refresh_token"] = token.refresh_token

    spotify_user = asyncio.run(
        spotify.get_current_user(token.access_token)
    )

    user, created = User.objects.get_or_create(
        spotify_id=spotify_user.id,
        defaults={
            "username": spotify_user.id,
            "display_name": spotify_user.display_name or "",
            "country": spotify_user.country or "",
            "profile_url": (
                spotify_user.external_urls.spotify
                if spotify_user.external_urls
                else ""
            ),
            "profile_image": (
                spotify_user.images[0].url
                if spotify_user.images
                else ""
            ),
        },
    )

    django_login(request, user)

    return redirect("music")

@login_required
def music(request):
    return render(
        request,
        "library/music_loading.html",
    )


@login_required
async def music_fetch(request):
    access_token = request.session.get("access_token")

    if not access_token:
        return redirect("login")

    spotify_service = create_spotify_service()
    discogs_service = DiscogsService()

    service = MusicService(
        spotify_service=spotify_service,
        discogs_service=discogs_service,
    )

    await service.get_users_music(
        request.user,
        access_token,
    )

    return redirect("music_results")


@login_required
def music_results(request):

    albums = list(
        Album.objects.filter(
            user=request.user,
        ).prefetch_related(
            "discogs_marketplace_listings",
        )
    )

    return render(
        request,
        "library/music.html",
        {
            "albums": albums,
        },
    )