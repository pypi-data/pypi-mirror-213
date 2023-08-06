"""
"""

import bs4
import requests

from .quote_strip import QuoteStrip


class StockQuote:
    """
    :param symbol: The ticker symbol of the stock
    """
    url = "https://cnbc.com/quotes/{symbol}"

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.address = self.url.format(symbol=self.symbol)

        self._response = requests.get(self.address, timeout=100)
        self._soup = bs4.BeautifulSoup(self._response.text, features="lxml")

        self._quote_strip = QuoteStrip(self._soup)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbol={self.symbol}, address={self.address})"

    @property
    def quote_strip(self) -> QuoteStrip:
        """
        Returns the quote strip of the stock.
        """
        return self._quote_strip
