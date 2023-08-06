"""
"""

import datetime
import re
import typing

import bs4
import numpy as np


class QuoteStrip:
    """
    :param soup: The ``bs4.BeautifulSoup`` object containing the stock quote page content
    """
    def __init__(self, soup: bs4.BeautifulSoup):
        self._soup = soup

        self._container = self._soup.select_one("div#quote-page-strip")

    def __repr__(self) -> str:
        arg_names = (
            "market_open", "name", "symbol", "exchange", "last_trade_time",
            "last_price", "change", "change_pct", "volume", "ftweek_range",
            "ext_last_trade_time", "ext_last_price", "ext_change", "ext_change_pct", "ext_volume"
        )
        arguments = (f"{x}={self.__getattribute__(x)}" for x in arg_names)
        return f"{type(self).__name__}({', '.join(arguments)})"

    def __str__(self) -> str:
        return "{symbol}: {last_price} {change} ({change_pct})".format(
            symbol=self.symbol,
            last_price=(self.last_price if self.market_open else self.ext_last_price),
            change=(self.change if self.market_open else self.ext_change),
            change_pct=(self.change_pct if self.market_open else self.ext_change_pct)
        )

    @property
    def market_open(self) -> bool:
        """
        Returns whether the market is open.
        """
        element = self._container.select_one("div.QuoteStrip-lastTradeTime")
        return not element.text.strip() == "Close"

    @property
    def name(self) -> str:
        """
        Returns the name of the company of the stock.
        """
        element = self._container.select_one("span.QuoteStrip-name")
        return element.text.strip()

    @property
    def symbol(self) -> str:
        """
        Returns the ticker symbol of the stock.
        """
        element = self._container.select_one("span.QuoteStrip-symbolAndExchange")
        return element.text.split(":")[0].strip()

    @property
    def exchange(self) -> str:
        """
        Returns the exchange to which the stock belongs.
        """
        element = self._container.select_one("span.QuoteStrip-symbolAndExchange")
        return element.text.split(":")[1].strip()

    @property
    def last_trade_time(self) -> typing.Optional[datetime.datetime]:
        """
        Returns the last trade time of the stock.
        """
        if not self.market_open:
            return None

        element = self._container.select_one("div.QuoteStrip-lastTradeTime")
        return datetime.datetime.strptime(element.text.strip(), "Last | %I:%M %p EDT")

    @property
    def last_price(self) -> float:
        """
        Returns the last price of the stock.
        """
        container = self._container.select_one(
            f"div.QuoteStrip-dataContainer:nth-child({3 if self.market_open else 4})"
        )
        element = container.select_one("span.QuoteStrip-lastPrice")
        return float(element.text.strip())

    @property
    def change(self) -> float:
        """
        Returns the change amount of the stock.
        """
        container = self._container.select_one(
            f"div.QuoteStrip-dataContainer:nth-child({3 if self.market_open else 4})"
        )
        element = container.select_one(
            "span.QuoteStrip-changeDown, span.QuoteStrip-changeUp, span.QuoteStrip-unchanged"
        )

        if "QuoteStrip-unchanged" in element.attrs.get("class"):
            return np.nan
        return float(element.select_one("span:nth-of-type(1)").text.strip())

    @property
    def change_pct(self) -> float:
        """
        Returns the percent change of the stock.
        """
        container = self._container.select_one(
            f"div.QuoteStrip-dataContainer:nth-child({3 if self.market_open else 4})"
        )
        element = container.select_one(
            "span.QuoteStrip-changeDown, span.QuoteStrip-changeUp, span.QuoteStrip-unchanged"
        )

        try:
            return float(
                re.search(
                    r"^\((.*)%\)$", element.select_one("span:nth-of-type(2)").text.strip()
                ).group(1)
            )
        except AttributeError:
            return np.nan

    @property
    def volume(self) -> int:
        """
        Returns the volume of the stock.
        """
        container = self._container.select_one(
            f"div.QuoteStrip-dataContainer:nth-child({3 if self.market_open else 4})"
        )
        element = container.select_one("div.QuoteStrip-volume")
        return int("".join(element.text.strip().split(",")))

    @property
    def ftweek_range(self) -> typing.Tuple[float, float]:
        """
        Returns the 52-week range of the stock.
        """
        element = self._container.select_one("div.QuoteStrip-fiftyTwoWeekRange")
        return tuple(map(lambda x: float(x.strip()), element.text.strip().split("-")))

    @property
    def ext_last_trade_time(self) -> typing.Optional[datetime.datetime]:
        """
        Extended hours version of :py:attr:`QuoteStrip.last_trade_time`.
        """
        if self.market_open:
            return None

        element = self._container.select_one(
            "div.QuoteStrip-extendedLastTradeTime > span:nth-of-type(2)"
        )
        return datetime.datetime.strptime(element.text.strip(), "Last | %I:%M %p EDT")

    @property
    def ext_last_price(self) -> float:
        """
        Extended hours version of :py:attr:`QuoteStrip.last_price`.
        """
        if self.market_open:
            return np.nan

        container = self._container.select_one("div.QuoteStrip-dataContainer:nth-child(3)")
        element = container.select_one("span.QuoteStrip-lastPrice")
        return float(element.text.strip())

    @property
    def ext_change(self) -> float:
        """
        Extended hours version of :py:attr:`QuoteStrip.change`.
        """
        if self.market_open:
            return np.nan

        container = self._container.select_one("div.QuoteStrip-dataContainer:nth-child(3)")
        element = container.select_one(
            "span.QuoteStrip-changeDown, span.QuoteStrip-changeUp, span.QuoteStrip-unchanged"
        )

        if "QuoteStrip-unchanged" in element.attrs.get("class"):
            return np.nan
        return float(element.select_one("span:nth-of-type(1)").text.strip())

    @property
    def ext_change_pct(self) -> float:
        """
        Extended hours version of :py:attr:`QuoteStrip.change_pct`.
        """
        if self.market_open:
            return np.nan

        container = self._container.select_one("div.QuoteStrip-dataContainer:nth-child(3)")
        element = container.select_one(
            "span.QuoteStrip-changeDown, span.QuoteStrip-changeUp, span.QuoteStrip-unchanged"
        )

        try:
            return float(
                re.search(
                    r"^\((.*)%\)$", element.select_one("span:nth-of-type(2)").text.strip()
                ).group(1)
            )
        except AttributeError:
            return np.nan

    @property
    def ext_volume(self) -> int:
        """
        Extended hours version of :py:attr:`QuoteStrip.volume`.
        """
        if self.market_open:
            return None

        container = self._container.select_one("div.QuoteStrip-dataContainer:nth-child(3)")
        element = container.select_one("div.QuoteStrip-volume")
        return int("".join(element.text.strip().split(",")))
