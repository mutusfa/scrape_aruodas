from scrape_aruodas.spiders.rent import (
    get_next_page_url,
    get_page_num_from_url,
    parse_breadcrums_url,
    parse_directions_url,
)


def test_get_page_num_from_url():
    assert get_page_num_from_url("https://www.aruodas.lt/butu-nuoma/puslapis/10/") == 10


def test_get_page_num_from_url_first_page():
    assert get_page_num_from_url("https://www.aruodas.lt/butu-nuoma/") == 1


def test_get_next_page_url():
    assert get_next_page_url("https://www.aruodas.lt/butu-nuoma/puslapis/10/") == (
        "https://www.aruodas.lt/butu-nuoma/puslapis/11/"
    )
    assert get_next_page_url("https://www.aruodas.lt/butu-nuoma/puslapis/2/") == (
        "https://www.aruodas.lt/butu-nuoma/puslapis/3/"
    )


def test_get_next_page_url_first_page():
    assert get_next_page_url("https://www.aruodas.lt/butu-nuoma/") == (
        "https://www.aruodas.lt/butu-nuoma/puslapis/2/"
    )


def test_parse_breadcrums_url():
    assert parse_breadcrums_url("/butu-nuoma/vilniuje/zirmunuose/kalvariju-g/") == (
        "vilniuje",
        "zirmunuose",
        "kalvariju-g",
    )


def test_parse_directions_url():
    assert parse_directions_url(
        "https://maps.google.lt?saddr=Current+Location&daddr=(54.716137,25.288044)"
    ) == (54.716137, 25.288044)
