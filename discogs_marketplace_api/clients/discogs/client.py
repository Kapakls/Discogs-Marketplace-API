import cloudscraper


class DiscogsClient:

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def search_marketplace(
        self,
        artist: str,
        album: str,
    ) -> str:

        search_query = (
            f"{artist.replace(' ', '+')}+"
            f"{album.replace(' ', '+')}"
        )

        url = (
            "https://www.discogs.com/sell/list"
            f"?q={search_query}"
            "&page=1"
            "&per_page=25"
        )

        response = self.scraper.get(url)

        response.raise_for_status()

        return response.text

    def close(self):
        self.scraper.close()