# Scrapy project for aruodas.lt scraping

This project will scrape information on listings from aruodas.lt
Currently scraped features are:

- Location:
  - city
  - district
  - street
  - latitude
  - longitude
- Size:
  - floor area
  - number of rooms
- Building information:
  - floor
  - number of floors in thie building
  - year of building
  - building material
  - type of heating
- price (for rent it's monthly rent price)
- listing_url


## Installation

```
git clone git@github.com:mutusfa/scrape_aruodas.git
cd scrape_aruodas
pip install
# run tests
pytest
scrapy check
```

## Usage

```
scrapy crawl rent -o scraped_data/rent.json
```
Would scrape listings of rent and put it into `scraped_data/rent.json` directory.

Listing available spiders:
```
scrapy list
```

## Configuration

Scraping settings can be changed by modifying `src/scrape_aruodas/settings.py`
Spiders are located in `src/scrape_aruodas/spiders`
