import sys

from monads import Option, some, nada

# Try to import necessary PIP packages
try:
    import datetime as dt
    import requests as rq
    import bs4 as bs
except ImportError:
    print("This script requires the following pip packages:")
    print("- bs4")
    print("- requests")
    print("- datetime")
    sys.exit(1)


class ScraperException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class Scraper:
    """Scrape a website"""
    site: rq.Response

    def __init__(self, website: str) -> None:
        self.site = rq.get(website)

        if not self.is_ok():
            raise ScraperException(f"Site '{website}' not available for scraping.'")

    def is_ok(self) -> bool:
        try:
            self.site.raise_for_status()
        except rq.exceptions.HTTPError:
            return False

        return True

    def scrape_selector(self, selector: str) -> Option[str]:
        """Scrape a website and get text from an element using specified selector"""

        # Parse website as a BeautifulSoup object and get tags from the passed selector
        soup = bs.BeautifulSoup(self.site.content, 'html.parser')
        tags = soup.select(selector)

        # Return the first tag's text if it is present, otherwise show an error and return nada
        if len(tags) > 0:
            return some(tags[0].getText())
        else:
            return nada()
