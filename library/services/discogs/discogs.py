import requests

from library.services.discogs.schemas.marketplace import MarketplaceListing


class DiscogsService:
    BASE_URL = "http://127.0.0.1:8001"

    def search_marketplace(
        self,
        album,
    ) -> list[MarketplaceListing]:

        response = requests.get(
            f"{self.BASE_URL}/marketplace/match",
            params={
                "artist": album.artist,
                "album": album.title,
                "threshold": 0.1,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return []

        data = response.json()

        return [
            MarketplaceListing.model_validate(item)
            for item in data["listings"]
        ]