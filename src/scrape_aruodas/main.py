import tempfile
from typing import IO, Tuple

import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from scrape_aruodas.spiders.rent import RentSpider

configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})


def _settings_to_feed_to_tmp_file() -> Tuple[dict, IO]:
    tmp_file = tempfile.NamedTemporaryFile()
    feed_settings = {
        tmp_file.name: {
            "format": "csv",
        }
    }
    return feed_settings, tmp_file


def scrape(num_items=3000):
    settings = get_project_settings()
    settings.set("CLOSESPIDER_ITEMCOUNT", num_items)
    feed_settings, temp_file = _settings_to_feed_to_tmp_file()
    settings.set("FEEDS", feed_settings)
    process = CrawlerProcess(settings)
    d = process.crawl(RentSpider)
    reactor.run()
    return pd.read_csv(temp_file.name)


if __name__ == "__main__":
    scrape("stuff")