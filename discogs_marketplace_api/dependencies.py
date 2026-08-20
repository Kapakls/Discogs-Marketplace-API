from discogs_marketplace_api.clients.discogs.client import (
    DiscogsClient,
)
from discogs_marketplace_api.clients.discogs.parser import (
    DiscogsParser,
)
from discogs_marketplace_api.services.marketplace import (
    MarketplaceService,
)

discogs_client = DiscogsClient()
discogs_parser = DiscogsParser()

marketplace_service = MarketplaceService(
    client=discogs_client,
    parser=discogs_parser,
)   