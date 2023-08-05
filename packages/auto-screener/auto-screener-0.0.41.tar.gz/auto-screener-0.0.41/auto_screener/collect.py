# collect.py

import threading
from typing import (
    Optional, Dict, Iterable, List, Callable, Union, Any
)

from cryptofeed.feed import Feed

from auto_screener.exchanges import EXCHANGES
from auto_screener.symbols import (
    symbol_to_parts, Separator, parts_to_symbol, adjust_symbol
)

__all__ = [
    "collect_assets",
    "collect_symbols",
    "collect_mutual_assets",
    "collect_mutual_symbols",
    "is_valid_symbol",
    "validate_symbol",
    "collect_exchanges",
    "is_valid_exchange",
    "validate_exchange",
    "find_name"
]

def _collect_exchange_assets(
        data: Dict[str, List[str]],
        exchange: str,
        feed: Feed,
        separator: Optional[str] = Separator.value,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Iterable[str]] = None
) -> None:
    """
    Collects the tickers from the exchanges.

    :param exchange: The name of the exchange.
    :param feed: The exchange object.
    :param data: The data to collect the assets.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    quotes = quotes or []
    excluded = excluded or []
    assets = []

    try:
        exchange_symbols: Iterable[str] = feed.symbols()

    except Exception as e:
        data[exchange] = []

        raise RuntimeError(
            f"Cannot fetch symbols of '{exchange}' exchange."
        ) from e
    # end try

    for symbol in exchange_symbols:
        symbol = adjust_symbol(symbol=symbol, separator=separator)

        try:
            base, quote = symbol_to_parts(symbol=symbol)

        except ValueError:
            continue
        # end try

        if (
            (quotes and (find_name(name=quote, names=quotes) in quotes)) and
            not (excluded and (find_name(name=base, names=excluded) in excluded)) and
            not (excluded and (find_name(name=quote, names=excluded) in excluded))
        ):
            assets.append(base)
        # end if
    # end for

    data[exchange] = list(set(assets))
# end _collect_exchange_assets

def _collect_exchange_symbols(
        data: Dict[str, List[str]],
        exchange: str,
        feed: Feed,
        quotes: Optional[Iterable[str]] = None,
        separator: Optional[str] = Separator.value,
        excluded: Optional[Iterable[str]] = None
) -> None:
    """
    Collects the tickers from the exchanges.

    :param exchange: The name of the exchange.
    :param feed: The exchange object.
    :param data: The data to collect the assets.
    :param quotes: The quotes of the asset pairs.
    :param separator: The separator of the assets.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    quotes = quotes or []
    excluded = excluded or []
    symbols = []

    excluded = [
        adjust_symbol(symbol=symbol, separator=separator)
        for symbol in (excluded or [])
    ]

    try:
        exchange_symbols: Iterable[str] = feed.symbols()

    except Exception as e:
        data[exchange] = []

        raise RuntimeError(
            f"Cannot fetch symbols of '{exchange}' exchange."
        ) from e
    # end try

    for symbol in exchange_symbols:
        symbol = adjust_symbol(symbol=symbol, separator=separator)

        try:
            _, quote = symbol_to_parts(symbol=symbol)

        except ValueError:
            continue
        # end try

        if (
            (quotes and (find_name(name=quote, names=quotes) in quotes)) and
            not (excluded and (find_name(name=symbol, names=excluded) in excluded))
        ):
            symbols.append(symbol)
        # end if
    # end for

    data[exchange] = list(set(symbols))
# end _collect_exchange_symbols

Collector = Callable[
    [Dict[str, List[str]], str, Feed, Optional[Iterable[str]]], None
]

def find_name(name: str, names: Iterable[str]) -> str:
    """
    Finds the exchange in the exchanges.

    :param name: The name of the exchange.
    :param names: The exchanges to search in.

    :return: The valid exchange name.
    """

    if name.lower() in names:
        return name.lower()
    # end if

    if name.upper() in names:
        return name.upper()
    # end if

    for value in names:
        if value.lower() == name.lower():
            return value
        # end if
    # end for

    return name
# end find_name

def _collect_data(
        collector: Collector,
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    excluded_symbols = []

    excluded = excluded or {}

    if not excluded:
        excluded_symbols = excluded
    # end if

    if (
        excluded and
        all(isinstance(value, str) for value in excluded) and
        not isinstance(excluded, dict)
    ):
        excluded = {exchange: excluded_symbols for exchange in exchanges}
    # end if

    quotes = quotes or []
    exchanges = exchanges or EXCHANGES

    data = {}
    markets = {}

    for exchange in exchanges:
        exchange = find_name(name=exchange, names=EXCHANGES)

        if exchange not in EXCHANGES:
            continue
        # end if

        markets[exchange] = EXCHANGES[exchange]
    # end for

    for exchange, feed in markets.items():
        exchange = find_name(name=exchange, names=excluded)

        threading.Thread(
            target=collector,
            kwargs=dict(
                exchange=exchange, feed=feed,
                data=data, quotes=quotes, excluded=(
                    excluded[exchange] if exchange in excluded else None
                )
            )
        ).start()
    # end for

    while len(markets) > len(data):
        pass
    # end while

    return {key: value for key, value in data.items() if value}
# end collect_symbols

def collect_assets(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    return _collect_data(
        collector=_collect_exchange_assets,
        exchanges=exchanges, quotes=quotes, excluded=excluded
    )
# end collect_symbols

def _collect_mutual_data(
        data: Dict[str, Iterable[str]],
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param data: The exchanges' data.

    :return: The data of the exchanges.
    """

    values = {}

    for exchange in data:
        for value in data[exchange]:
            values[value] = values.setdefault(value, 0) + 1
        # end for
    # end for

    return {
        exchange: [
            value for value in data[exchange]
            if values.get(value, 0) > 1
        ] for exchange in data
    }
# end collect_mutual_assets

def collect_mutual_assets(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.
    :param data: The data to search in.

    :return: The data of the exchanges.
    """

    return _collect_mutual_data(
        data=data or collect_assets(
            exchanges=exchanges, quotes=quotes, excluded=excluded
        )
    )
# end collect_mutual_assets

def collect_symbols(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.

    :return: The data of the exchanges.
    """

    return _collect_data(
        collector=_collect_exchange_symbols,
        exchanges=exchanges, quotes=quotes, excluded=excluded
    )
# end collect_symbols

def collect_mutual_symbols(
        exchanges: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        data: Optional[Dict[str, Iterable[str]]] = None
) -> Dict[str, List[str]]:
    """
    Collects the tickers from the exchanges.

    :param exchanges: The exchanges.
    :param quotes: The quotes of the asset pairs.
    :param excluded: The excluded tickers.
    :param data: The data to search in.

    :return: The data of the exchanges.
    """

    return _collect_mutual_data(
        data=data or collect_symbols(
            exchanges=exchanges, quotes=quotes, excluded=excluded
        )
    )
# end collect_mutual_symbols

def is_valid_symbol(
        exchange: str,
        symbol: str,
        exchanges: Optional[Iterable[str]] = None,
        symbols: Optional[Iterable[str]] = None
) -> bool:
    """
    Returns a value for the symbol being valid for the source exchange.

    :param exchange: The name of the exchange platform.
    :param symbol: The symbol of the assets.
    :param symbols: The valid symbols.
    :param exchanges: The valid exchanges.

    :return: The validation-value.
    """

    if symbols is None:
        exchange = find_name(name=exchange, names=EXCHANGES)

        if not is_valid_exchange(
            exchange=exchange, exchanges=exchanges
        ):
            return False
        # end if

        symbols = EXCHANGES[exchange].symbols()
    # end for

    symbols = [adjust_symbol(symbol=s) for s in symbols]

    symbol = find_name(name=adjust_symbol(symbol=symbol), names=symbols)

    return symbol in symbols
# end is_valid_symbol

def validate_symbol(
        exchange: str,
        symbol: str,
        exchanges: Optional[Iterable[str]] = None,
        symbols: Optional[Iterable[str]] = None,
        provider: Optional[Any] = None
) -> str:
    """
    Returns a value for the symbol being valid for the source exchange.

    :param exchange: The name of the exchange platform.
    :param symbol: The symbol of the assets.
    :param symbols: The valid symbols.
    :param exchanges: The valid exchanges.
    :param provider: Any provider object.

    :return: The validation-value.
    """

    validate_exchange(
        exchange=exchange, exchanges=exchanges,
        provider=provider
    )

    if not is_valid_symbol(
        exchange=exchange, symbol=symbol, symbols=symbols
    ):
        raise ValueError(
            f"'{symbol}' is not a valid "
            f"symbol for the '{exchange}' exchange. "
            f"Valid symbols: {', '.join(symbols)}"
            f"{f' for {provider}.' if provider else ''}"
        )
    # end if

    return symbol
# end validate_symbol

def is_valid_exchange(exchange: str, exchanges: Optional[Iterable[str]] = None) -> bool:
    """
    checks of the source os a valid exchange name.

    :param exchange: The source name to validate.
    :param exchanges: The valid exchanges.

    :return: The validation value.
    """

    if exchanges is None:
        exchanges = EXCHANGES
    # end if

    return find_name(name=exchange, names=exchanges) in exchanges
# end is_valid_exchange

def validate_exchange(
        exchange: str,
        exchanges: Optional[Iterable[str]] = None,
        provider: Optional[Any] = None
) -> str:
    """
    Validates the source value.

    :param exchange: The name of the exchange platform.
    :param exchanges: The valid exchanges.
    :param provider: Any provider object.

    :return: The validates symbol.
    """

    if exchanges is None:
        exchanges = EXCHANGES
    # end if

    if not is_valid_exchange(exchange=exchange, exchanges=exchanges):
        raise ValueError(
            f"'{exchange}' is not a valid exchange name. "
            f"Valid exchanges: {', '.join(exchanges.keys())}"
            f"{f' for {provider}.' if provider else ''}"
        )
    # end if

    return exchange
# end validate_exchange

def collect_exchanges(
        currencies: Dict[str, List[str]],
        pairs: Dict[str, List[str]],
        excluded: Optional[Dict[str, Iterable[str]]] = None,
) -> Dict[str, List[str]]:
    """
    Collects the exchanges.

    :param pairs: The data of currencies and their traded quote assets.
    :param currencies: The data of exchanges and their traded currencies.
    :param excluded: The data of excluded pairs for each exchange.

    :return: The data of exchanges and their tickers.
    """

    exchanges: Dict[str, List[str]] = {}

    for platform, currencies in currencies.items():
        exchanges[platform] = []

        for currency in currencies:
            for asset in pairs[currency]:
                if (
                    parts_to_symbol(asset, currency) in
                    excluded.get(platform, [])
                ):
                    continue
                # end if

                exchanges[platform].append(
                    parts_to_symbol(asset, currency)
                )
            # end for
        # end for
    # end for

    return exchanges
# end collect_exchanges