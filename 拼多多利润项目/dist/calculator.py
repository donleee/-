# -*- coding: utf-8 -*-
"""
利润计算器模块
"""

class ProfitCalculator:
    """利润计算器类"""
    
    def __init__(self):
        """初始化计算器"""
        self.default_commission_rate = 0.02  # 默认佣金率2%
        self.default_shipping_cost = 5.0     # 默认运费5元
    
    def calculate_profit(self, selling_price, cost_price, quantity=1, 
                        commission_rate=None, shipping_cost=None,
                        packaging_cost=0.0, marketing_cost=0.0, other_costs=0.0):
        """计算商品利润"""
        if commission_rate is None:
            commission_rate = self.default_commission_rate
        if shipping_cost is None:
            shipping_cost = self.default_shipping_cost
        
        # 计算各项成本
        product_cost = cost_price * quantity
        commission = selling_price * quantity * commission_rate
        total_shipping_cost = shipping_cost * quantity
        total_packaging_cost = packaging_cost * quantity
        total_marketing_cost = marketing_cost
        total_other_costs = other_costs
        
        # 计算总收入
        total_revenue = selling_price * quantity
        
        # 计算总成本
        total_cost = (product_cost + commission + total_shipping_cost + 
                     total_packaging_cost + total_marketing_cost + total_other_costs)
        
        # 计算净利润
        net_profit = total_revenue - total_cost
        
        # 计算利润率
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'net_profit': net_profit,
            'profit_margin': profit_margin,
            'product_cost': product_cost,
            'commission': commission,
            'shipping_cost': total_shipping_cost,
            'packaging_cost': total_packaging_cost,
            'marketing_cost': total_marketing_cost,
            'other_costs': total_other_costs
        }
