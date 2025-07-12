from dataclasses import dataclass
from typing import Optional

def get_float_input(prompt, min_value=None, max_value=None, allow_empty=False):
    while True:
        val = input(prompt)
        if allow_empty and val.strip() == '':
            return None
        try:
            value = float(val)
            if min_value is not None and value < min_value:
                print(f"数值不能小于{min_value}")
                continue
            if max_value is not None and value > max_value:
                print(f"数值不能大于{max_value}")
                continue
            return value
        except ValueError:
            print("请输入有效数字！")

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
    refund_orders: Optional[float] = None  # 新增，退货数
    instant_refund_orders: Optional[float] = None  # 新增，秒退订单数

def collect_user_input():
    print("请输入以下参数（单位：元或百分比，百分比请直接输入数字，如5代表5%）：")
    price = float(get_float_input("商品售价: ", 0))
    cost = float(get_float_input("商品成本: ", 0))
    other_cost = float(get_float_input("其他成本: ", 0))
    shipping_fee = float(get_float_input("平均运费: ", 0))
    commission_rate = float(get_float_input("平台扣点(%): ", 0, 100)) / 100
    refund_rate = float(get_float_input("退款率(%): ", 0, 100)) / 100
    instant_refund_rate = float(get_float_input("秒退率(%): ", 0, 100)) / 100
    post_shipping_refund_ratio = float(get_float_input("发货后退款比例(%): ", 0, 100)) / 100
    ad_cpc_input = get_float_input("单次点击花费(元, 可选，默认0): ", 0, allow_empty=True)
    ad_cpc = float(ad_cpc_input) if ad_cpc_input is not None else 0.0
    ad_conversion_rate_input = get_float_input("转化率(%, 可选，默认0): ", 0, 100, allow_empty=True)
    ad_conversion_rate = float(ad_conversion_rate_input) / 100 if ad_conversion_rate_input is not None else 0.0
    order_count = int(get_float_input("模拟订单数: ", 1))
    refund_orders = get_float_input("退货数(可选，留空则自动计算): ", 0, allow_empty=True)
    instant_refund_orders = get_float_input("秒退订单数(可选，留空则自动计算): ", 0, allow_empty=True)
    kwargs = {}
    if refund_orders is not None:
        kwargs['refund_orders'] = float(refund_orders)
    if instant_refund_orders is not None:
        kwargs['instant_refund_orders'] = float(instant_refund_orders)
    return ProfitInput(
        price, cost, other_cost, shipping_fee, commission_rate,
        refund_rate, instant_refund_rate, post_shipping_refund_ratio,
        ad_cpc, ad_conversion_rate, **kwargs
    ), order_count 