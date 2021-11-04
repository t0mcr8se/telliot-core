from typing import Any
from typing import Optional


from telliot.datafeed.pricing.price_service import WebPriceService
from telliot.types.datapoint import DataPoint, OptionalDataPoint, datetime_now_utc


class CoinbasePriceService(WebPriceService):
    """Coinbase Price Service"""

    def __init__(self, **kwargs: Any) -> None:
        kwargs["name"] = "Coinbase Price Service"
        kwargs["url"] = "https://api.pro.coinbase.com"
        super().__init__(**kwargs)

    async def get_price(self, asset: str, currency: str) -> OptionalDataPoint[float]:
        """Implement PriceServiceInterface

        This implementation gets the price from the Coinbase pro API
        using the interface described at:
        https://docs.pro.coinbase.com/#products API

        Note that the timestamp returned form the coinbase API could be used
        instead of the locally generated timestamp.
        """

        request_url = "/products/{}-{}/ticker".format(asset.lower(), currency.lower())

        d = self.get_url(request_url)
        if "error" in d:
            print(d)  # TODO: Log
            return None, None

        elif "response" in d:
            response = d["response"]

            if "message" in response:
                print("API ERROR ({}): {}".format(self.name, response["message"]))
                return None, None

        else:
            raise Exception("Invalid response from get_url")

        price = float(response["price"])
        return price, datetime_now_utc()
