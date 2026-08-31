from fastapi import APIRouter

from dependencies import marketplace_service
from schemas.marketplace import MarketplaceMatchResponse

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