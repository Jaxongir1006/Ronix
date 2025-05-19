import urllib.parse
from dataclasses import dataclass
from decimal import Decimal
from django.conf import settings


@dataclass
class GenerateClickLink:
    order_id: str
    amount: Decimal

    def generate_link(self) -> str:
        """
        Generate a Click payment link.
        """
        params = {
            "service_id": settings.CLICK_SERVICE_ID,
            "merchant_id": settings.CLICK_MERCHANT_ID,
            "transaction_param": self.order_id,
            "amount": str(self.amount),  # e.g. '10000'
            "return_url": settings.CLICK_RETURN_URL,
        }

        query_string = urllib.parse.urlencode(params)
        return f"{settings.CLICK_PAYMENT_URL}?{query_string}"