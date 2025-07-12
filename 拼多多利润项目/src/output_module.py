import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from typing import Dict

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def print_profit_report(result: Dict):
    """打印利润分析报告"""
    print("\n" + "="*50)
    print("📊 拼多多利润分析报告")
    print("="*50)
    
    # 显示商品型号
    if '商品型号' in result:
        print(f"🏷️  商品型号: {result['商品型号']}")
        print("-" * 50)
    
    print(f"📈 总利润: {result['总利润']:.2f} 元")
    print(f"💰 单均利润: {result['单均利润']:.2f} 元")
    print(f"📊 利润率: {result['利润率']:.2f}%")
    print(f"💸 总收入: {result['总收入']:.2f} 元")
    print(f"💳 总成本: {result['总成本']:.2f} 元")
    print(f"🎯 保本售价: {result['保本售价']:.2f} 元")
    
    if result.get('广告启用', False):
        print(f"📢 广告费用: {result['广告费用']:.2f} 元")
        print(f"💰 每单广告出价: {result['每单广告出价']:.2f} 元")
        if result['保本广告出价'] is not None:
            print(f"⚠️  保本广告出价: {result['保本广告出价']:.2f} 元/单")
        if result['保本ROI'] is not None:
            print(f"📊 保本ROI: {result['保本ROI']:.2f}")
        if result['当前ROI'] is not None:
            print(f"📈 当前ROI: {result['当前ROI']:.2f}")
    
    print(f"\n📦 订单数据:")
    print(f"   分析订单数: {result['订单总数']}")
    print(f"   销量: {result['销量']}")
    print(f"   退货数量: {result['退货数量']}")
    print(f"   成交订单数: {result['成交订单数']}")
    print(f"   净成交订单数: {result['净成交订单数']}")
    print(f"   退款率: {result['退款率']:.2f}%")
    print(f"   秒退率: {result['秒退率']:.2f}%")
    
    print(f"\n💰 成本构成:")
    for item, cost in result['成本构成'].items():
        print(f"   {item}: {cost:.2f} 元")
    
    # 显示详细计算公式
    if '计算公式' in result:
        print(f"\n🧮 详细计算公式:")
        formulas = result['计算公式']
        
        print(f"  📦 订单分析:")
        for key, formula in formulas['订单分析'].items():
            print(f"     {key}: {formula}")
        
        print(f"  💰 收入计算:")
        for key, formula in formulas['收入计算'].items():
            print(f"     {key}: {formula}")
        
        print(f"  💳 成本计算:")
        for key, formula in formulas['成本计算'].items():
            print(f"     {key}: {formula}")
        
        print(f"  📊 利润计算:")
        for key, formula in formulas['利润计算'].items():
            print(f"     {key}: {formula}")
        
        print(f"  🎯 保本分析:")
        for key, formula in formulas['保本分析'].items():
            print(f"     {key}: {formula}")
    
    print("="*50)

def plot_cost_breakdown(cost_breakdown: Dict):
    """绘制成本构成饼图"""
    labels = list(cost_breakdown.keys())
    values = list(cost_breakdown.values())
    
    plt.figure(figsize=(10, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('成本构成分析')
    plt.axis('equal')
    plt.show()

def create_streamlit_report(result: Dict):
    """创建Streamlit报告界面"""
    st.subheader("📊 利润分析报告")
    
    # 显示商品型号
    if '商品型号' in result:
        st.info(f"🏷️ 商品型号: **{result['商品型号']}**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="总利润",
            value=f"{result['总利润']:.2f} 元",
            delta=f"{result['利润率']:.1f}%"
        )
    
    with col2:
        st.metric(
            label="单均利润",
            value=f"{result['单均利润']:.2f} 元"
        )
    
    with col3:
        st.metric(
            label="保本售价",
            value=f"{result['保本售价']:.2f} 元"
        )
    
    with col4:
        if result.get('广告启用', False):
            st.metric(
                label="广告出价",
                value=f"{result['每单广告出价']:.2f} 元/单"
            )
        else:
            st.metric(
                label="广告出价",
                value="未启用"
            )
    
    # 显示退款率和秒退率
    st.subheader("📈 实时数据分析")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            label="退款率",
            value=f"{result['退款率']:.2f}%",
            help="退款率 = 退货数量 ÷ 销量 × 100%"
        )
    
    with metric_col2:
        st.metric(
            label="秒退率",
            value=f"{result['秒退率']:.2f}%",
            help="秒退率 = (成交订单 - 净成交订单) ÷ 成交订单 × 100%"
        )
    
    with metric_col3:
        st.metric(
            label="成交订单",
            value=f"{result['成交订单数']}",
            help="实际成交的订单数量"
        )
    
    with metric_col4:
        st.metric(
            label="净成交订单",
            value=f"{result['净成交订单数']}",
            help="最终完成交易的订单数量"
        )
    
    # 新增ROI指标显示
    if result.get('广告启用', False):
        st.subheader("📈 ROI分析")
        col5, col6 = st.columns(2)
        
        with col5:
            if result.get('当前ROI') is not None:
                st.metric(
                    label="当前ROI",
                    value=f"{result['当前ROI']:.2f}",
                    help="当前ROI = 当前售价 ÷ 当前广告出价"
                )
        
        with col6:
            if result.get('保本ROI') is not None:
                st.metric(
                    label="保本ROI",
                    value=f"{result['保本ROI']:.2f}",
                    help="保本ROI = 保本售价 ÷ 保本广告出价"
                )
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.subheader("📈 成本构成分析")
        cost_data = result['成本构成']
        fig = px.pie(
            values=list(cost_data.values()),
            names=list(cost_data.keys()),
            title="成本构成占比"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col8:
        st.subheader("📦 订单情况")
        order_data = {
            '销量': result['销量'],
            '退货数量': result['退货数量'],
            '成交订单': result['成交订单数'],
            '净成交订单': result['净成交订单数']
        }
        
        fig = px.bar(
            x=list(order_data.keys()),
            y=list(order_data.values()),
            title="订单数据分布"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💰 详细财务数据")
    financial_data = {
        '项目': ['商品型号', '销量', '退货数量', '成交订单数', '净成交订单数', '退款率', '秒退率', '总收入', '总成本', '总利润', '利润率', '保本售价'],
        '数值': [
            result.get('商品型号', 'N/A'),
            str(result['销量']),
            str(result['退货数量']),
            str(result['成交订单数']),
            str(result['净成交订单数']),
            f"{result['退款率']:.2f}%",
            f"{result['秒退率']:.2f}%",
            f"{result['总收入']:.2f} 元",
            f"{result['总成本']:.2f} 元",
            f"{result['总利润']:.2f} 元",
            f"{result['利润率']:.2f}%",
            f"{result['保本售价']:.2f} 元"
        ]
    }
    
    if result.get('广告启用', False):
        financial_data['项目'].extend(['广告费用', '保本广告出价', '当前ROI', '保本ROI'])
        financial_data['数值'].extend([
            f"{result['广告费用']:.2f} 元",
            f"{result['保本广告出价']:.2f} 元" if result['保本广告出价'] is not None else "N/A",
            f"{result['当前ROI']:.2f}" if result['当前ROI'] is not None else "N/A",
            f"{result['保本ROI']:.2f}" if result['保本ROI'] is not None else "N/A"
        ])
    
    df = pd.DataFrame(financial_data)
    st.table(df)
    
    if result.get('广告启用', False) and result['保本广告出价'] is not None:
        st.info(f"💡 保本广告出价: {result['保本广告出价']:.2f} 元/单")
        if result['保本广告出价'] < result.get('每单广告出价', 0):
            st.warning("⚠️ 当前广告出价已超过保本线，建议优化广告策略")
    
    # 显示计算公式
    if '计算公式' in result:
        with st.expander("🧮 查看详细计算公式"):
            formulas = result['计算公式']
            
            st.write("**📦 订单分析:**")
            for key, formula in formulas['订单分析'].items():
                st.write(f"- {key}: `{formula}`")
            
            st.write("**💰 收入计算:**")
            for key, formula in formulas['收入计算'].items():
                st.write(f"- {key}: `{formula}`")
            
            st.write("**💳 成本计算:**")
            for key, formula in formulas['成本计算'].items():
                st.write(f"- {key}: `{formula}`")
            
            st.write("**📊 利润计算:**")
            for key, formula in formulas['利润计算'].items():
                st.write(f"- {key}: `{formula}`")
            
            st.write("**🎯 保本分析:**")
            for key, formula in formulas['保本分析'].items():
                st.write(f"- {key}: `{formula}`")

def create_profit_trend_chart(prices: list, profits: list):
    """创建利润趋势图"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prices,
        y=profits,
        mode='lines+markers',
        name='利润',
        line=dict(color='green', width=2)
    ))
    
    fig.update_layout(
        title='不同售价下的利润变化',
        xaxis_title='售价 (元)',
        yaxis_title='利润 (元)',
        hovermode='x unified'
    )
    
    return fig

def export_to_excel(result: Dict, filename: str = "profit_analysis.xlsx"):
    """导出结果到Excel"""
    import pandas as pd
    
    summary_data = {
        '指标': ['商品型号', '销量', '退货数量', '成交订单数', '净成交订单数', '退款率', '秒退率', '总利润', '单均利润', '利润率', '总收入', '总成本', '保本售价'],
        '数值': [
            result.get('商品型号', 'N/A'),
            result['销量'],
            result['退货数量'],
            result['成交订单数'],
            result['净成交订单数'],
            f"{result['退款率']:.2f}%",
            f"{result['秒退率']:.2f}%",
            result['总利润'],
            result['单均利润'],
            result['利润率'],
            result['总收入'],
            result['总成本'],
            result['保本售价']
        ]
    }
    
    if result.get('广告启用', False):
        summary_data['指标'].extend(['广告费用', '保本广告出价', '当前ROI', '保本ROI'])
        summary_data['数值'].extend([
            result['广告费用'],
            result['保本广告出价'] if result['保本广告出价'] is not None else 0,
            result['当前ROI'] if result['当前ROI'] is not None else 0,
            result['保本ROI'] if result['保本ROI'] is not None else 0
        ])
    
    cost_data = pd.DataFrame(list(result['成本构成'].items()), columns=['成本项目', '金额'])
    
    # 计算公式数据
    formulas_data = []
    if '计算公式' in result:
        formulas = result['计算公式']
        for category, category_formulas in formulas.items():
            for key, formula in category_formulas.items():
                formulas_data.append({
                    '分类': category,
                    '项目': key,
                    '计算公式': formula
                })
    
    with pd.ExcelWriter(filename) as writer:
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='利润汇总', index=False)
        cost_data.to_excel(writer, sheet_name='成本明细', index=False)
        if formulas_data:
            pd.DataFrame(formulas_data).to_excel(writer, sheet_name='计算公式', index=False)
    
    return filename 