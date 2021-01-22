import re
from typing import Dict, List, Tuple

import scrapy
from scrapy.item import Item, Field


class RentListing(Item):
    # location
    city = Field()
    district = Field()
    street = Field()
    # a dict of distances to objects of interest
    # doesn't show for scrapy :(
    distances = Field()
    latitude = Field()
    longitude = Field()

    # misc
    listing_url = Field()
    object_details = Field()  # a dict of details, will need to be processed later
    number_of_crimes_within_500_meters = Field()


def get_page_num_from_url(url: str) -> int:
    try:
        return int(url.split("/")[-2])
    except ValueError:
        return 1


def get_next_page_url(url: str) -> str:
    split_url = url.split("/")
    current_page = split_url[-2]
    try:
        next_page = int(current_page) + 1
    except ValueError:
        return "https://www.aruodas.lt/butu-nuoma/puslapis/2/"
    split_url[-2] = str(next_page)
    return "/".join(split_url)


def parse_breadcrums_url(url: str) -> Tuple[str, str, str]:
    split_url = url.split("/")
    return split_url[-4], split_url[-3], split_url[-2]


def get_distances_from_response(response: scrapy.http.Response) -> Dict[str, str]:
    distances_keys = response.xpath(
        '//div[contains(@class, "statistic-info-row")][@data-type="distance"]'
        '//span[contains(@class, "cell-text")]/text()'
    ).getall()
    distances_values = response.xpath(
        '//div[contains(@class, "statistic-info-row")][@data-type="distance"]'
        '//span[contains(@class, "cell-data")]/text()'
    ).getall()
    return dict(zip(distances_keys, distances_values))


def get_object_details_from_response(response: scrapy.http.Response) -> Dict[str, str]:
    obj_details_xpath = '//dl[contains(@class, "obj-details")]'
    obj_details_keys = response.xpath(f"{obj_details_xpath}/dt/text()").getall()
    obj_details_values = response.xpath(f"{obj_details_xpath}/dd/text()").getall()
    return dict(
        ((k.strip(), v.strip()) for (k, v) in zip(obj_details_keys, obj_details_values))
    )


def parse_directions_url(url: str) -> Tuple[float, float]:
    try:
        match = re.search(
            r"&daddr=\((?P<long>\d{1,3}\.\d+),(?P<lat>\d{1,3}\.\d+)\)$", url
        )
    except TypeError:
        raise TypeError(f"{url} is of type {type(url)}, expected str or bytes-str")
    return float(match["long"]), float(match["lat"])  # type: ignore


class RentSpider(scrapy.Spider):
    name = "rent"
    allowed_domains = ["aruodas.lt"]
    start_urls = ["https://www.aruodas.lt/butu-nuoma/"]

    def _is_last_search_page(self, response):
        buttons = response.xpath(
            '//div[contains(@class,"pagination")]/a/text()'
        ).getall()
        # exclude < and > buttons
        last_page_in_button = max(int(b) for b in buttons[1:-1])
        current_page = get_page_num_from_url(response.url)
        return last_page_in_button == current_page

    def parse(self, response):
        """Main parsing loop.

        Goes through the catalog of all rent listings.
        Delegates parsing of listings to parse_listing.

        @url https://www.aruodas.lt/butu-nuoma/
        @returns items 0 0
        @returns requests 10
        """
        if self._is_last_search_page(response):
            return

        # find all the listings
        listing_url_regex = r"-(?P<listing_id>\d+)/$"
        urls = response.xpath("//a/@href").getall()
        for url in urls:
            if re.search(listing_url_regex, url):
                yield response.follow(url, callback=self.parse_listing)
        yield scrapy.Request(get_next_page_url(response.url), callback=self.parse)

    def parse_listing(self, response):
        """Parse a single listing.

        @url https://www.aruodas.lt/butu-nuoma-vilniuje-zirmunuose-kalvariju-g-ramioje-vietoje-zirmunuose-kalvariju-g-4-1005091/
        @returns items 1 1
        @scrapes city district listing_url

        """
        # location
        breadcrums_url = response.xpath(
            '//div[contains(@class, "obj-breadcrums")]' "//meta[@content=5]/../a/@href"
        ).get()
        city, district, street = parse_breadcrums_url(breadcrums_url)
        distances = get_distances_from_response(response)
        directions_url = response.xpath('//a[@data-type="directions"]/@href').get()
        if directions_url:
            latitude, longitude = parse_directions_url(directions_url)

        # misc
        listing_url = response.url
        object_details = get_object_details_from_response(response)
        number_of_crimes_within_500_meters = response.xpath(
            '//div[@class="icon-crime-gray"]/../span[@class="cell-data"]/text()'
        )

        local_vars = locals()
        rent_listing = RentListing()
        for field in rent_listing.fields:
            try:
                rent_listing[field] = local_vars[field]
            except KeyError:
                pass
        return rent_listing
