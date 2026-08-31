from clients.discogs.client import (
    DiscogsClient,
)
from clients.discogs.parser import (
    DiscogsParser,
)
from services.marketplace import (
    MarketplaceService,
)

discogs_client = DiscogsClient()
discogs_parser = DiscogsParser()

marketplace_service = MarketplaceService(
    client=discogs_client,
    parser=discogs_parser,
)   