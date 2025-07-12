from dataclasses import dataclass
from typing import Optional

@dataclass
class ProfitInput:
    price: float
    cost: float
    other_cost: float
    shipping_fee: float
    commission_rate: float
    refund_rate: float
    instant_refund_rate: float
    post_shipping_refund_ratio: float
    ad_cpc: float = 0.0
    ad_conversion_rate: float = 0.0
    refund_orders: Optional[float] = None
    instant_refund_orders: Optional[float] = None 