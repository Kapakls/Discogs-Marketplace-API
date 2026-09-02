from fastapi import APIRouter

from dependencies import marketplace_service
from schemas.marketplace import (
    BatchMatchRequest,
    MarketplaceMatchResponse,
)

router = APIRouter()


@router.get(
    "/match",
    response_model=MarketplaceMatchResponse,
)
def match_album(
    artist: str,
    album: str,
    threshold: float = 0.1,
):
    return marketplace_service.find_matches_for_album(
        artist=artist,
        album=album,
        threshold=threshold,
    )

@router.post(
    "/match/batch",
    response_model=list[MarketplaceMatchResponse],
)
async def match_album_batch(request: BatchMatchRequest):

    albums = [
        (album.artist, album.album)
        for album in request.albums
    ]

    results = await marketplace_service.find_matches_for_multiple_albums(albums)

    return results