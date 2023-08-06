# tickers.py

from typing import (
    Optional, Tuple, Dict,
    Any, List, Iterable, Union
)

from represent import BaseModel, Modifiers

__all__ = [
    "Pair",
    "symbol_to_pair",
    "symbol_to_parts",
    "pair_to_symbol",
    "parts_to_symbol",
    "reverse_symbol",
    "reverse_pair",
    "adjust_symbol",
    "parts_to_pair",
    "pair_to_parts",
    "symbols_to_parts",
    "parts_to_symbol_parts",
    "parts_to_symbol_parts",
    "assets_to_symbols",
    "parts_to_symbols",
    "Separator"
]

class Separator:
    """A class to contain the separator value."""

    value = "/"
# end Separator

class Pair(BaseModel):
    """
    A class to represent a trading pair.

    This object represents a pair of assets that can be traded.

    attributes:

    - base:
        The asset to buy or sell.

    - quote:
        The asset to use to buy or sell.

    >>> from auto_screener.symbols import Pair
    >>>
    >>> pair = Pair("BTC", "USD")
    """

    modifiers = Modifiers(excluded=["parts"])

    __slots__ = "base", "quote", "parts"

    def __init__(self, base: str, quote: str) -> None:
        """
        Defines the class attributes.

        :param base: The base asset of the trading pair.
        :param quote: The target asset of the trading pair.
        """

        self.base = base
        self.quote = quote

        self.parts = (self.base, self.quote)
    # end __init__

    def __getitem__(self, item: Union[slice, int]) -> Union[str, Iterable[str]]:
        """
        Returns the items.

        :param item: The slice item.

        :return: The items in the object to get with the slice.
        """

        data = self.parts[item]

        if isinstance(data, list):
            # noinspection PyTypeChecker
            return type(self)(*data)
        # end if

        return data
    # end __getitem__

    def __len__(self) -> int:
        """
        The length of the assets.

        :return: The length of the assets.
        """

        return len(self.parts)
    # end __len__

    def __iter__(self) -> Iterable[str]:
        """
        Returns the object as an iterable.

        :return: The iterable object.
        """

        yield from self.parts
    # end __iter__

    @staticmethod
    def load(parts: Iterable[str]):
        """
        Creates a pair of assets from the data.

        :param parts: The pair data.

        :return: The pair object.
        """

        if not (
            (len(tuple(parts)) == 2) and
            all(isinstance(part, str) for part in parts)
        ):
            raise ValueError(
                f"Pair data must be an iterable of base asset and "
                f"quote asset of type str, in that order, not {parts}."
            )
        # end if

        return Pair(*parts)
    # end load

    def symbol(self) -> str:
        """
        Gets the tickers of the chain.

        :return: The tickers of the trading chain.
        """

        return pair_to_symbol(self)
    # end tickers

    def json(self) -> Tuple[str, str]:
        """
        Converts the data into a json format.

        :return: The chain of assets.
        """

        return pair_to_parts(self)
    # end json
# end Pair

def pair_to_symbol(pair: Pair, separator: Optional[str] = Separator.value) -> str:
    """
    Converts a pair of assets into a symbol.

    :param pair: The pair of assets.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    if separator is None:
        separator = Separator.value
    # end if

    return f"{pair.base}{separator}{pair.quote}"
# end pair_to_symbol

def parts_to_symbol(base: str, quote: str, separator: Optional[str] = Separator.value) -> str:
    """
    Converts a pair of assets into a symbol.

    :param base: The base assets.
    :param quote: The quote assets.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    if separator is None:
        separator = Separator.value
    # end if

    return f"{base}{separator}{quote}"
# end parts_to_symbol

def symbol_to_pair(symbol: str, separator: Optional[str] = Separator.value) -> Pair:
    """
    Converts a pair of assets into a symbol.

    :param symbol: The symbol to convert into a pair object.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    if separator is None:
        separator = Separator.value
    # end if

    if separator in symbol:
        base = symbol[:symbol.find(separator)]
        quote = symbol[symbol.find(separator) + len(separator):]

    else:
        raise ValueError(
            f"Cannot separate symbol '{symbol}' because "
            f"the given separator '{separator}' is not in the symbol."
        )
    # end if

    return Pair(base=base, quote=quote)
# end symbol_to_pair

def parts_to_pair(base: str, quote: str) -> Pair:
    """
    Converts a pair of assets into a symbol.

    :param base: The base assets.
    :param quote: The quote assets.

    :return: The symbol.
    """

    return Pair(base, quote)
# end parts_to_pair

def symbol_to_parts(symbol: str, separator: Optional[str] = Separator.value) -> Tuple[str, str]:
    """
    Converts a pair of assets into a symbol.

    :param symbol: The symbol to convert into a pair object.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    pair = symbol_to_pair(symbol=symbol, separator=separator)

    return pair.base, pair.quote
# end symbol_to_parts

def reverse_symbol(symbol: str, separator: Optional[str] = Separator.value) -> str:
    """
    Converts a pair of assets into a symbol.

    :param symbol: The symbol to convert into a pair object.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    return parts_to_symbol(base=quote, quote=base)
# end reverse_symbol

def reverse_pair(pair: Pair, separator: Optional[str] = Separator.value) -> Pair:
    """
    Converts a pair of assets into a symbol.

    :param pair: The pair of assets.
    :param separator: The separator of the assets.

    :return: The symbol.
    """

    return symbol_to_pair(
        reverse_symbol(
            symbol=pair_to_symbol(pair=pair, separator=separator),
            separator=separator
        )
    )
# end symbol_to_parts

def pair_to_parts(pair: Pair) -> Tuple[str, str]:
    """
    Converts a pair of assets into a symbol.

    :param pair: The pair of assets.

    :return: The symbol.
    """

    return pair.base, pair.quote
# end pair_to_parts

def adjust_symbol(symbol: str, separator: Optional[str] = Separator.value) -> str:
    """
    Adjusts the symbol of the asset.

    :param symbol: The symbol of the asset to adjust.
    :param separator: The separator of the assets.

    :return: The adjusted asset symbol.
    """

    if separator is None:
        separator = Separator.value
    # end if

    if separator is None:
        separator = Separator.value
    # end if

    return symbol.replace("-", separator)
# end adjust_symbol

def symbols_to_parts(symbols: Dict[str, Dict[str, Any]]) -> Tuple[List[str], List[str]]:
    """
    Collects the bases and quotes of the tickers.

    :param symbols: The tickers to separate.

    :return: The separated bases and quotes.
    """

    quotes = []
    bases = []

    for base in symbols:
        if base not in bases:
            bases.append(base)
        # end if

        for quote in symbols[base]:
            if quote not in quotes:
                quotes.append(quote)
            # end if
        # end for
    # end for

    return bases, quotes
# end symbols_to_parts

def parts_to_symbol_parts(
        bases: Iterable[str],
        quotes: Iterable[str],
        symbols: Optional[Dict[str, Dict[str, Any]]] = None
) -> List[Tuple[str, str]]:
    """
    Collects the bases and quotes of the tickers.

    :param bases: The bases to join.
    :param quotes: The quotes to join.
    :param symbols: The tickers to separate.

    :return: The joined tickers.
    """

    pairs = []

    for base in bases:
        for quote in quotes:
            if (
                ((base, quote) not in pairs) and
                (
                    (
                        (symbols is not None) and
                        (quote in symbols[base])
                    ) or (symbols is None)
                )
            ):
                pairs.append((base, quote))
            # end if
        # end for
    # end for

    return pairs
# end parts_to_symbol_parts

def parts_to_symbols(
        bases: Iterable[str],
        quotes: Iterable[str],
        symbols: Optional[Dict[str, Dict[str, Any]]] = None
) -> List[str]:
    """
    Collects the bases and quotes of the tickers.

    :param bases: The bases to join.
    :param quotes: The quotes to join.
    :param symbols: The tickers to separate.

    :return: The joined tickers.
    """

    return [
        parts_to_symbol(*parts) for parts in
        (parts_to_symbol_parts(bases, quotes, symbols))
    ]
# end parts_to_symbols

def assets_to_symbols(assets: Iterable[str]) -> List[str]:
    """
    Creates the tickers from the assets.

    :param assets: The asset to build the tickers from.

    :return: The list of tickers.
    """

    tickers = []

    for base in assets:
        for quote in assets:
            ticker = parts_to_symbol(base, quote)

            if base != quote and reverse_symbol(ticker) not in tickers:
                tickers.append(ticker)
            # end if
        # end for
    # end for

    return tickers
# end assets_to_symbols