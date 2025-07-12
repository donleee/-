from typing import Dict
from .input_module import ProfitInput

def calculate_profit(inputs: ProfitInput, order_count: int = 100) -> Dict:
    """
    拼多多利润计算引擎 - 基于净成交广告出价的版本
    
    计算公式说明：
    1. 订单分析：
       - 销量: 用户输入
       - 退货数量: 用户输入
       - 成交订单: 用户输入 (仅用于显示和秒退率计算)
       - 净成交订单: 用户输入 (仅用于显示)
       - 退款率 = 退货数量 ÷ 销量 × 100%
       - 秒退率 = (成交订单 - 净成交订单) ÷ 成交订单 × 100%
    
    2. 收入计算：
       - 实际收入 = 分析订单数 × 商品售价
    
    3. 成本计算：
       - 商品成本 = 分析订单数 × (商品成本 + 其他成本)
       - 运费成本 = 分析订单数 × 运费
       - 平台扣点 = 实际收入 × 平台扣点率
       - 广告费用 = 分析订单数 × 每笔广告出价
       - 退款广告损失 = 每笔广告出价 × 退款率
       - 总成本 = 商品成本 + 运费成本 + 平台扣点 + 广告费用 + 退款广告损失
    
    4. 利润计算：
       - 总利润 = 实际收入 - 总成本
       - 单均利润 = 总利润 ÷ 分析订单数
       - 利润率 = (总利润 ÷ 实际收入) × 100%
    
    5. 保本分析：
       - 保本广告出价 = 售价×(1-扣点率) - 商品成本 - 其他成本 - 运费
       - 保本售价 = (商品成本 + 其他成本 + 运费 + 广告出价) ÷ (1 - 平台扣点率)
       - 最高广告投入 = 保本广告出价 × (1 - 退款率)
       - 保本ROI = 保本售价 ÷ 保本广告出价
    
    注意: 净成交订单数仅用于显示，不参与任何利润计算；所有计算均基于分析订单数
    """
    
    # === 1. 订单分析计算 ===
    # 直接使用用户输入的数据
    total_orders = order_count  # 分析的订单基数
    sales_volume = inputs.sales_volume  # 销量
    return_quantity = inputs.return_quantity  # 退货数量
    deal_orders = inputs.deal_orders  # 成交订单
    net_deal_orders = inputs.net_deal_orders  # 净成交订单
    
    # 计算实时的退款率和秒退率
    refund_rate = inputs.refund_rate  # 已通过@property计算
    instant_refund_rate = inputs.instant_refund_rate  # 已通过@property计算
    
    # === 2. 收入计算 ===
    # 公式：实际收入 = 分析订单数 × 商品售价
    actual_revenue = total_orders * inputs.price
    
    # === 3. 成本计算 ===
    # 公式：商品成本 = 分析订单数 × (商品成本 + 其他成本)
    total_product_cost = total_orders * (inputs.cost + inputs.other_cost)
    # 公式：运费成本 = 分析订单数 × 运费
    total_shipping_cost = total_orders * inputs.shipping_fee
    # 公式：平台扣点 = 实际收入 × 平台扣点率
    commission = actual_revenue * inputs.commission_rate
    
    # 公式：广告费用 = 分析订单数 × 每笔广告出价
    ad_cost = 0.0
    if inputs.ad_enabled and inputs.ad_deal_price > 0:
        ad_cost = total_orders * inputs.ad_deal_price

    # 公式：退款广告损失 = 每笔广告出价 × 退款率
    refund_ad_loss = 0.0
    if inputs.ad_enabled and inputs.ad_deal_price > 0:
        refund_ad_loss = inputs.ad_deal_price * refund_rate

    # 公式：总成本 = 商品成本 + 运费成本 + 平台扣点 + 广告费用 + 退款广告损失
    total_cost = total_product_cost + total_shipping_cost + commission + ad_cost + refund_ad_loss
    
    # === 4. 利润计算 ===
    # 公式：总利润 = 实际收入 - 总成本
    final_profit = actual_revenue - total_cost
    # 公式：单均利润 = 总利润 ÷ 分析订单数
    profit_per_order = final_profit / total_orders if total_orders else 0
    # 公式：利润率 = (总利润 ÷ 实际收入) × 100%
    profit_rate = (final_profit / actual_revenue * 100) if actual_revenue != 0 else 0

    # === 5. 保本分析计算 ===
    # 公式：保本广告出价 = 售价×(1-扣点率) - 商品成本 - 其他成本 - 运费
    max_ad_deal_price = inputs.price * (1 - inputs.commission_rate) - inputs.cost - inputs.other_cost - inputs.shipping_fee
    max_ad_deal_price = max(0, max_ad_deal_price)
    
    # 公式：保本售价 = (商品成本 + 其他成本 + 运费 + 广告出价) ÷ (1 - 平台扣点率)
    unit_cost = inputs.cost + inputs.other_cost + inputs.shipping_fee
    if inputs.ad_enabled:
        # 不考虑退款率的广告费用
        unit_cost += inputs.ad_deal_price
    
    if (1 - inputs.commission_rate) > 0:
        break_even_price = unit_cost / (1 - inputs.commission_rate)
    else:
        break_even_price = 0

    # 公式：最高广告投入 = 保本广告出价 × (1 - 退款率)
    max_ad_investment = None
    break_even_roi = None
    if inputs.ad_enabled:
        max_ad_investment = max_ad_deal_price * (1 - refund_rate)
        
        # 公式：保本ROI = 保本售价 ÷ 保本广告出价
        if max_ad_deal_price > 0:
            break_even_roi = break_even_price / max_ad_deal_price
        else:
            break_even_roi = 0
    
    # 当前ROI计算（如果启用广告）
    current_roi = None
    if inputs.ad_enabled and inputs.ad_deal_price > 0:
        # 公式：当前ROI = 当前售价 ÷ 当前广告出价
        current_roi = inputs.price / inputs.ad_deal_price

    # 成本构成
    cost_breakdown = {
        '商品成本': total_product_cost,
        '运费': total_shipping_cost,
        '平台扣点': commission
    }
    
    if ad_cost > 0:
        cost_breakdown['广告费用'] = ad_cost
    
    if refund_ad_loss > 0:
        cost_breakdown['退款广告损失'] = refund_ad_loss

    return {
        '商品型号': inputs.model_name,
        '总利润': final_profit,
        '单均利润': profit_per_order,
        '利润率': profit_rate,
        '总收入': actual_revenue,
        '总成本': total_cost,
        '成本构成': cost_breakdown,
        '保本售价': break_even_price,
        '保本广告出价': max_ad_deal_price,
        '最高广告投入': max_ad_investment,
        '保本ROI': break_even_roi,
        '当前ROI': current_roi,
        '订单总数': total_orders,
        '销量': sales_volume,
        '退货数量': return_quantity,
        '成交订单数': deal_orders,
        '净成交订单数': net_deal_orders,
        '退款率': refund_rate * 100,  # 转换为百分比显示
        '秒退率': instant_refund_rate * 100,  # 转换为百分比显示
        '广告费用': ad_cost,
        '广告启用': inputs.ad_enabled,
        '每单广告出价': inputs.ad_deal_price if inputs.ad_enabled else 0,
        # 添加计算公式说明
        '计算公式': {
            '订单分析': {
                '销量': f'{sales_volume}',
                '退货数量': f'{return_quantity}',
                '成交订单数': f'{deal_orders}',
                '净成交订单数': f'{net_deal_orders}',
                '退款率': f'{return_quantity} ÷ {sales_volume} × 100% = {refund_rate * 100:.2f}%',
                '秒退率': f'({deal_orders} - {net_deal_orders}) ÷ {deal_orders} × 100% = {instant_refund_rate * 100:.2f}%'
            },
            '收入计算': {
                '实际收入': f'{total_orders} × {inputs.price} = {actual_revenue:.2f}'
            },
            '成本计算': {
                '商品成本': f'{total_orders} × ({inputs.cost} + {inputs.other_cost}) = {total_product_cost:.2f}',
                '运费成本': f'{total_orders} × {inputs.shipping_fee} = {total_shipping_cost:.2f}',
                '平台扣点': f'{actual_revenue:.2f} × {inputs.commission_rate} = {commission:.2f}',
                '广告费用': f'{total_orders} × {inputs.ad_deal_price} = {ad_cost:.2f}' if inputs.ad_enabled else '未启用广告',
                '退款广告损失': f'{inputs.ad_deal_price} × {refund_rate:.2%} = {refund_ad_loss:.2f}' if inputs.ad_enabled else '未启用广告',
                '总成本': f'{total_product_cost:.2f} + {total_shipping_cost:.2f} + {commission:.2f} + {ad_cost:.2f} + {refund_ad_loss:.2f} = {total_cost:.2f}'
            },
            '利润计算': {
                '总利润': f'{actual_revenue:.2f} - {total_cost:.2f} = {final_profit:.2f}',
                '利润率': f'({final_profit:.2f} ÷ {actual_revenue:.2f}) × 100% = {profit_rate:.2f}%'
            },
            '保本分析': {
                '保本售价': f'({inputs.cost} + {inputs.other_cost} + {inputs.shipping_fee} + {inputs.ad_deal_price if inputs.ad_enabled else 0:.2f}) ÷ (1 - {inputs.commission_rate}) = {break_even_price:.2f}',
                '保本广告出价': f'{inputs.price} × (1 - {inputs.commission_rate}) - {inputs.cost} - {inputs.other_cost} - {inputs.shipping_fee} = {max_ad_deal_price:.2f}' if max_ad_deal_price is not None else '未启用广告',
                '最高广告投入': f'{max_ad_deal_price:.2f} × (1 - {refund_rate:.2%}) = {max_ad_investment:.2f}' if max_ad_investment is not None else '未启用广告',
                '保本ROI': f'{break_even_price:.2f} ÷ {max_ad_deal_price:.2f} = {break_even_roi:.2f}' if break_even_roi is not None else '未启用广告',
                '当前ROI': f'{inputs.price} ÷ {inputs.ad_deal_price} = {current_roi:.2f}' if current_roi is not None else '未启用广告'
            }
        }
    } 