from typing import Dict
from .input_module import ProfitInput

def calculate_profit(inputs: ProfitInput, order_count: int = 100) -> Dict:
    # 1. 订单流程拆解
    total_orders = order_count
    instant_refund_orders = total_orders * inputs.instant_refund_rate
    after_instant_orders = total_orders - instant_refund_orders
    refund_orders = total_orders * inputs.refund_rate
    # 发货后退款订单数 = 进入发货流程订单数 × 发货后退款比例
    post_ship_refund_orders = after_instant_orders * inputs.post_shipping_refund_ratio
    # 发货前退款订单数 = 总退款订单数 - 发货后退款订单数
    pre_ship_refund_orders = refund_orders - post_ship_refund_orders
    # 成功交易订单数 = 进入发货流程订单数 - 发货后退款订单数
    success_orders = after_instant_orders - post_ship_refund_orders

    # 2. 收入
    actual_revenue = success_orders * inputs.price

    # 3. 成本
    # 商品成本和其他成本：所有发货的订单都产生
    total_product_cost = after_instant_orders * (inputs.cost + inputs.other_cost)
    # 运费：所有发货的订单都产生
    total_shipping_cost = after_instant_orders * inputs.shipping_fee
    # 平台扣点：只对实际成交订单收取
    commission = actual_revenue * inputs.commission_rate

    # 4. 利润
    total_cost = total_product_cost + total_shipping_cost + commission
    final_profit = actual_revenue - total_cost
    profit_per_order = final_profit / total_orders
    profit_rate = (final_profit / actual_revenue * 100) if actual_revenue != 0 else 0

    # 5. 保本售价
    # 保本售价 = (商品成本+其他成本+运费) / (1-平台扣点费率)
    if (1 - inputs.commission_rate) > 0:
        break_even_price = (inputs.cost + inputs.other_cost + inputs.shipping_fee) / (1 - inputs.commission_rate)
    else:
        break_even_price = 0

    # 6. 保本投产比
    if inputs.ad_cpc > 0 and inputs.ad_conversion_rate > 0:
        break_even_roi = break_even_price / (inputs.ad_cpc / inputs.ad_conversion_rate)
    else:
        break_even_roi = None

    # 7. 成本构成
    cost_breakdown = {
        '商品成本': total_product_cost,
        '运费': total_shipping_cost,
        '平台扣点': commission
    }

    return {
        '总利润': final_profit,
        '单均利润': profit_per_order,
        '利润率': profit_rate,
        '总收入': actual_revenue,
        '总成本': total_cost,
        '成本构成': cost_breakdown,
        '保本售价': break_even_price,
        '保本投产比': break_even_roi,
        '订单总数': total_orders,
        '成功交易订单数': success_orders,
        '秒退订单数': instant_refund_orders,
        '退款订单数': refund_orders
    } 