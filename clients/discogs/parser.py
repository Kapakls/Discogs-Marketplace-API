import pycountry
from bs4 import BeautifulSoup

from schemas.marketplace import MarketplaceListing


class DiscogsParser:

    def parse(self, html: str) -> list[MarketplaceListing]:
        soup = BeautifulSoup(html, "lxml")

        listings = soup.find_all(
            "tr",
            class_=[
                "shortcut_navigable",
                "shortcut_navigable unavailable",
            ],
        )

        results = []

        for item in listings:
            listing = MarketplaceListing(
                title=self.parse_title(item),
                price=self.parse_price(item),
                currency=self.parse_currency(item),
                listing_id=self.parse_listing_id(item),
                listing_url=self.parse_listing_url(item),
                seller_country=self.parse_seller_country(item),
                media_condition=self.parse_media_condition(item),
                sleeve_condition=self.parse_sleeve_condition(item),
                seller_rating=self.parse_seller_rating(item),
            )

            results.append(listing)

        return results

    @staticmethod
    def parse_title(item) -> str:
        element = item.select_one(".item_description_title")

        return element.get_text(strip=True) if element else ""

    @staticmethod
    def parse_price(item) -> float:
        element = item.select_one(".price")

        if not element:
            return 0.0

        return float(element.get("data-pricevalue", "0"))

    @staticmethod
    def parse_currency(item) -> str:
        element = item.select_one(".price")

        if not element:
            return ""

        return element.get("data-currency", "")

    @staticmethod
    def parse_listing_id(item) -> str:
        element = item.select_one(".cart-button")

        if not element:
            return ""

        return element.get("data-item-id", "")

    @staticmethod
    def parse_listing_url(item) -> str:
        element = item.select_one(".item_description_title")

        if not element:
            return ""

        href = element.get("href", "")

        return f"https://www.discogs.com{href}"

    @staticmethod
    def parse_seller_country(item) -> str:
        element = item.select_one(
            '.seller_info li:-soup-contains("Ships From:")'
        )

        if not element:
            return ""

        country = element.get_text(strip=True).replace(
            "Ships From:",
            "",
        )

        result = pycountry.countries.get(name=country)

        return result.alpha_2 if result else ""

    @staticmethod
    def parse_media_condition(item) -> str:
        element = item.select_one(
            ".item_condition span:not(.mplabel)"
        )

        return element.get_text(strip=True) if element else ""

    @staticmethod
    def parse_sleeve_condition(item) -> str:
        element = item.select_one(".item_sleeve_condition")

        return element.get_text(strip=True) if element else ""

    @staticmethod
    def parse_seller_rating(item) -> float:
        element = item.select_one(
            ".seller_info .star_rating + strong"
        )

        if not element:
            return 0.0

        return float(
            element.get_text(strip=True).replace("%", "")
        )