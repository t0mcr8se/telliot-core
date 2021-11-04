"""Example datafeeds used by BTCUSDReporter."""
import statistics

from telliot.datafeed.pricing.price_source import PriceSource
from telliot.queries.coin_price import CoinPrice
from telliot_examples.coinprices.bittrex import BittrexPriceService
from telliot_examples.coinprices.coinbase import CoinbasePriceService
from telliot_examples.coinprices.coingecko import CoinGeckoPriceService
from telliot_examples.coinprices.gemini import GeminiPriceService
from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.pricing.price_feed import AggregatePriceSource


data_sources = [
    PriceSource(
        asset="btc",
        currency="usd",
        service=CoinbasePriceService(),
    ),
    PriceSource(
        asset="btc",
        currency="usd",
        service=CoinGeckoPriceService(),
    ),
    PriceSource(
        asset="btc",
        currency="usd",
        service=BittrexPriceService(),
    ),
    PriceSource(
        asset="btc",
        currency="usd",
        service=GeminiPriceService(),
    ),
]

target_query = CoinPrice(coin="btc", currency="usd", price_type="current")


btc_usd_median_feed = DataFeed(
    query=CoinPrice(coin="btc", currency="usd", price_type="current"),
    source=AggregatePriceSource(sources=data_sources,
                                asset='btc',
                                currency='usd',
                                algorithm=statistics.median)
)


