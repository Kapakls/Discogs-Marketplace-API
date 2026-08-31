from discogs_marketplace_api.clients.discogs.client import DiscogsClient
from discogs_marketplace_api.clients.discogs.parser import DiscogsParser
from discogs_marketplace_api.schemas.marketplace import (
    MarketplaceListing,
    MarketplaceMatchResponse,
)


class MarketplaceService:

    def __init__(
        self,
        client: DiscogsClient,
        parser: DiscogsParser,
    ):
        self.client = client
        self.parser = parser

    def find_matches(
        self,
        artist: str,
        album: str,
        threshold: float = 0.1,
    ) -> MarketplaceMatchResponse:

        html = self.client.search_marketplace(
            artist=artist,
            album=album,
        )

        listings = self.parser.parse(html)

        matches = []

        for listing in listings:
            similarity = self.calculate_similarity(
                album,
                listing.title,
            )

            if similarity >= threshold:
                matches.append(
                    MarketplaceListing(
                        title=listing.title,
                        price=listing.price,
                        currency=listing.currency,
                        listing_id=listing.listing_id,
                        listing_url=listing.listing_url,
                        seller_country=listing.seller_country,
                        media_condition=listing.media_condition,
                        sleeve_condition=listing.sleeve_condition,
                        seller_rating=listing.seller_rating,
                        similarity=similarity,
                    )
                )

        return MarketplaceMatchResponse(
            album=album,
            threshold=threshold,
            total=len(matches),
            listings=matches,
        )

    @staticmethod
    def calculate_similarity(
        album: str,
        listing: str,
    ) -> float:

        album_words = {
            word.lower()
            for word in album.split()
            if "-" not in word
        }

        listing_words = {
            word.lower()
            for word in listing.split()
            if "-" not in word
        }

        union = album_words | listing_words

        if not union:
            return 0.0

        intersection = album_words & listing_words

        return len(intersection) / len(union)