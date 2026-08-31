from fastapi import APIRouter

from discogs_marketplace_api.dependencies import marketplace_service
from discogs_marketplace_api.schemas.marketplace import MarketplaceMatchResponse

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
    return marketplace_service.find_matches(
        artist=artist,
        album=album,
        threshold=threshold,
    )