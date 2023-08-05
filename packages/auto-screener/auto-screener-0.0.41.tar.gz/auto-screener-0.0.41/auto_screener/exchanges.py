# exchanges.py

from cryptofeed.exchanges import EXCHANGE_MAP

__all__ = [
    "EXCHANGES"
]

EXCHANGES = {
    name.lower(): exchange
    for name, exchange in EXCHANGE_MAP.items()
}