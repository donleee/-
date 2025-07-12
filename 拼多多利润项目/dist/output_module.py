import matplotlib.pyplot as plt

def print_profit_report(result: dict):
    print("\n==== 利润计算结果 ====")
    print(f"总利润: {result['总利润']:.2f} 元")
    print(f"单均利润: {result['单均利润']:.2f} 元")
    print(f"利润率: {result['利润率']:.2f} %")
    print(f"总收入: {result['总收入']:.2f} 元")
    print(f"总成本: {result['总成本']:.2f} 元")
    print(f"成功交易订单数: {result['成功交易订单数']} / {result['订单总数']}")
    # 新增销量、退货数、退款率、秒退率、成交数、净成交数
    sales = result['订单总数']
    instant_refund_orders = result.get('秒退订单数', 0)
    refund_orders = result.get('退款订单数', 0)
    net_sales = sales - instant_refund_orders
    net_success_orders = result['成功交易订单数']
    print(f"销量: {sales}")
    print(f"退货数: {refund_orders}")
    print(f"退款率: {refund_orders / sales * 100:.2f} %")
    print(f"秒退订单数: {instant_refund_orders}")
    print(f"秒退率: {instant_refund_orders / sales * 100:.2f} %")
    print(f"成交数(发货数): {net_sales}")
    print(f"净成交数(最终成功交易): {net_success_orders}")
    print(f"保本售价: {result['保本售价']:.2f} 元")
    if result['保本投产比'] is not None:
        print(f"保本投产比: {result['保本投产比']:.2f}")
    print("\n成本构成:")
    for k, v in result['成本构成'].items():
        print(f"  {k}: {v:.2f} 元")

def plot_cost_breakdown(cost_breakdown: dict):
    labels = list(cost_breakdown.keys())
    sizes = list(cost_breakdown.values())
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('成本构成分析')
    plt.axis('equal')
    plt.show() 