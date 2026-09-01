# Discogs Marketplace API

A FastAPI-based API that searches the Discogs Marketplace for album listings and identifies potential matches using title similarity.

The API accepts an artist and album name, retrieves relevant Marketplace listings, parses their information, and calculates a similarity score to determine which listings are potential matches.

## Features

* Searches the Discogs Marketplace using artist and album information.
* Calculates similarity between an album title and listing titles using Jaccard similarity.
* Configurable similarity threshold for filtering results.
* Response containing multiple listings along with their seller, pricing, condition, and similarity information.

## Stack/Libraries

* Python 3.x
* FastAPI
* Uvicorn
* Cloudsraper
* BeautifulSoup4
* pycountry

## Requirements

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

## Running the API

Start the application using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Usage

The main endpoint accepts an artist, album, and optional similarity threshold.

For example:

```text
GET /marketplace?artist=Pink%20Floyd&album=The%20Dark%20Side%20of%20the%20Moon&threshold=0.1
```

The API searches the Discogs Marketplace for listings matching the provided artist and album, then filters the results based on the calculated similarity score.

A response contains the requested album, threshold, number of matching listings, and an list of matching Marketplace listings:

```json
{
    "album": "The Dark Side of the Moon",
    "threshold": 0.1,
    "total": 1,
    "listings": [
        {
            "title": "Pink Floyd - The Dark Side Of The Moon",
            "price": 25.00,
            "currency": "EUR",
            "listing_id": 123456789,
            "listing_url": "https://www.discogs.com/sell/item/123456789",
            "seller_country": "GR",
            "media_condition": "Very Good Plus (VG+)",
            "sleeve_condition": "Very Good Plus (VG+)",
            "seller_rating": 99.8,
            "similarity": 0.75
        }
    ]
}
```

## Matching Algorithm

The API as of now uses really simple Jaccard similarity to compare the requested album title with each Discogs Marketplace listing title.

The titles are split into individual words  with the similarity itself being calculated as:

```text
similarity = |intersection| / |union|
```

A configurable threshold determines whether a listing is included in the response.

For example, with a threshold of `0.5`, only listings with a similarity score of `0.5` or higher will be returned.

## Architecture

The API separates its responsibilities into different components:

* `MarketplaceService` — contains the marketplace matching and similarity logic.
* `DiscogsClient` — handles communication with the Discogs Marketplace.
* `DiscogsParser` — parses Marketplace HTML into structured listing data.
* `schemas` — defines the structured API request and response models.

## Disclaimer

This project is a created for personal use and development purposes.

It uses Discogs Marketplace data through web scraping and relies on third-party Python libraries. Please refer to the [Discogs Terms of Service](https://support.discogs.com/hc/en-us/articles/360009334333-Terms-of-Service) before using this API.
