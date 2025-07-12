from dataclasses import dataclass
from typing import Optional
import streamlit as st

@dataclass
class ProfitInput:
    model_name: str  # 商品型号
    price: float  # 商品售价
    cost: float  # 商品成本
    other_cost: float  # 其他成本
    shipping_fee: float  # 运费
    commission_rate: float  # 平台扣点（直接数字，如3表示3%）
    sales_volume: int  # 销量
    return_quantity: int  # 退货数量
    deal_orders: int  # 成交订单
    net_deal_orders: int  # 净成交订单
    post_shipping_refund_ratio: float = 0.0  # 发货后退款比例（保留字段）
    ad_deal_price: float = 0.0  # 成交出价：每笔净成交的广告费用
    ad_enabled: bool = False  # 是否启用广告
    
    @property
    def refund_rate(self) -> float:
        """计算退款率 = 退货数量/销量"""
        return self.return_quantity / self.sales_volume if self.sales_volume > 0 else 0
    
    @property
    def instant_refund_rate(self) -> float:
        """计算秒退率 = (成交订单-净成交订单)/成交订单"""
        return (self.deal_orders - self.net_deal_orders) / self.deal_orders if self.deal_orders > 0 else 0

def collect_user_input() -> ProfitInput:
    """收集用户输入的商品信息"""
    print("请输入商品信息：")
    
    model_name = input("商品型号: ")
    price = float(input("商品售价 (元): "))
    cost = float(input("商品成本 (元): "))
    other_cost = float(input("其他成本 (元): "))
    shipping_fee = float(input("运费 (元): "))
    commission_rate = float(input("平台扣点 (直接输入数字，如3表示3%): "))
    
    print("\n📊 订单数据:")
    sales_volume = int(input("销量: "))
    return_quantity = int(input("退货数量: "))
    deal_orders = int(input("成交订单: "))
    net_deal_orders = int(input("净成交订单: "))
    
    # 计算并显示实时退款率和秒退率
    refund_rate = (return_quantity / sales_volume * 100) if sales_volume > 0 else 0
    instant_refund_rate = ((deal_orders - net_deal_orders) / deal_orders * 100) if deal_orders > 0 else 0
    print(f"\n📈 实时计算:")
    print(f"退款率: {refund_rate:.2f}%")
    print(f"秒退率: {instant_refund_rate:.2f}%")
    
    ad_enabled_input = input("\n是否启用广告? (y/n): ").lower().strip()
    ad_enabled = ad_enabled_input in ['y', 'yes', '是']
    
    ad_deal_price = 0.0
    if ad_enabled:
        ad_deal_price = float(input("每笔净成交的广告出价 (元): "))
    
    return ProfitInput(
        model_name=model_name,
        price=price,
        cost=cost,
        other_cost=other_cost,
        shipping_fee=shipping_fee,
        commission_rate=commission_rate / 100,  # 转换为小数
        sales_volume=sales_volume,
        return_quantity=return_quantity,
        deal_orders=deal_orders,
        net_deal_orders=net_deal_orders,
        post_shipping_refund_ratio=0.0,
        ad_deal_price=ad_deal_price,
        ad_enabled=ad_enabled
    )

def collect_streamlit_input() -> ProfitInput:
    """在Streamlit界面收集用户输入"""
    st.subheader("📊 商品基本信息")
    
    model_name = st.text_input("商品型号", value="SKU001", help="输入商品的型号或SKU")
    
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("商品售价 (元)", min_value=0.0, value=100.0, step=0.01)
        cost = st.number_input("商品成本 (元)", min_value=0.0, value=50.0, step=0.01)
        other_cost = st.number_input("其他成本 (元)", min_value=0.0, value=5.0, step=0.01)
        shipping_fee = st.number_input("运费 (元)", min_value=0.0, value=10.0, step=0.01)
    
    with col2:
        commission_rate = st.number_input("平台扣点 (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, help="直接输入百分比数字，如3表示3%")
    
    st.subheader("📦 订单数据")
    col3, col4 = st.columns(2)
    with col3:
        sales_volume = st.number_input("销量", min_value=0, value=100, step=1)
        return_quantity = st.number_input("退货数量", min_value=0, value=10, step=1)
    
    with col4:
        deal_orders = st.number_input("成交订单", min_value=0, value=95, step=1)
        net_deal_orders = st.number_input("净成交订单", min_value=0, value=90, step=1)
    
    # 实时计算并显示退款率和秒退率
    refund_rate = (return_quantity / sales_volume * 100) if sales_volume > 0 else 0
    instant_refund_rate = ((deal_orders - net_deal_orders) / deal_orders * 100) if deal_orders > 0 else 0
    
    st.subheader("📈 实时计算")
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.metric(
            label="退款率",
            value=f"{refund_rate:.2f}%",
            help="退款率 = 退货数量 ÷ 销量 × 100%"
        )
    with metric_col2:
        st.metric(
            label="秒退率", 
            value=f"{instant_refund_rate:.2f}%",
            help="秒退率 = (成交订单 - 净成交订单) ÷ 成交订单 × 100%"
        )
    
    st.subheader("📈 广告信息")
    col5, col6 = st.columns(2)
    with col5:
        ad_enabled = st.checkbox("启用广告", value=False)
    with col6:
        ad_deal_price = st.number_input(
            "每笔净成交的广告出价 (元)", 
            min_value=0.0, 
            value=0.0, 
            step=0.01,
            disabled=not ad_enabled,
            help="成交出价模式：只对实际净成交（有效成交）收取广告费用"
        )
    
    if ad_enabled and ad_deal_price == 0:
        st.warning("⚠️ 已启用广告但未设置广告出价")
    
    return ProfitInput(
        model_name=model_name,
        price=price,
        cost=cost,
        other_cost=other_cost,
        shipping_fee=shipping_fee,
        commission_rate=commission_rate / 100,  # 转换为小数
        sales_volume=sales_volume,
        return_quantity=return_quantity,
        deal_orders=deal_orders,
        net_deal_orders=net_deal_orders,
        post_shipping_refund_ratio=0.0,
        ad_deal_price=ad_deal_price,
        ad_enabled=ad_enabled
    ) 