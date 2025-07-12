import streamlit as st
import pandas as pd
from src.input_module import collect_streamlit_input
from src.calculation_engine import calculate_profit
from src.output_module import create_streamlit_report, create_profit_trend_chart, export_to_excel
from src.history_manager import history_manager
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="拼多多利润分析系统",
    page_icon="💰",
    layout="wide"
)

def main():
    st.title("💰 拼多多利润分析系统")
    st.markdown("---")
    
    with st.sidebar:
        st.header("🛠️ 功能选择")
        mode = st.selectbox(
            "选择功能",
            ["单品利润分析", "批量分析", "利润趋势分析", "历史数据管理"]
        )
        
        st.header("📊 分析设置")
        order_count = st.number_input(
            "分析订单数量",
            min_value=1,
            max_value=10000,
            value=100,
            step=1
        )
    
    if mode == "单品利润分析":
        st.header("📊 单品利润分析")
        
        user_input = collect_streamlit_input()
        
        if st.button("🔍 计算利润", type="primary"):
            result = calculate_profit(user_input, order_count)
            
            # 自动保存到历史记录
            input_dict = {
                'model_name': user_input.model_name,
                'price': user_input.price,
                'cost': user_input.cost,
                'other_cost': user_input.other_cost,
                'shipping_fee': user_input.shipping_fee,
                'commission_rate': user_input.commission_rate,
                'sales_volume': user_input.sales_volume,
                'return_quantity': user_input.return_quantity,
                'deal_orders': user_input.deal_orders,
                'net_deal_orders': user_input.net_deal_orders,
                'ad_deal_price': user_input.ad_deal_price,
                'ad_enabled': user_input.ad_enabled,
                'analysis_orders': order_count
            }
            
            analysis_id = history_manager.save_analysis(input_dict, result)
            
            st.success(f"✅ 计算完成! 已保存到历史记录，ID: {analysis_id}")
            create_streamlit_report(result)
            
            if st.button("📥 导出Excel报告"):
                filename = export_to_excel(result)
                st.success(f"✅ 报告已导出: {filename}")
    
    elif mode == "批量分析":
        st.header("📊 批量商品分析")
        
        uploaded_file = st.file_uploader("上传CSV文件", type=['csv'])
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("📋 数据预览:")
            st.dataframe(df.head())
            
            if st.button("🔍 批量计算"):
                results = []
                for _, row in df.iterrows():
                    from src.input_module import ProfitInput
                    input_data = ProfitInput(
                        model_name=row.get('model_name', f'SKU-{_}'),
                        price=row.get('price', 0),
                        cost=row.get('cost', 0),
                        other_cost=row.get('other_cost', 0),
                        shipping_fee=row.get('shipping_fee', 0),
                        commission_rate=row.get('commission_rate', 0) / 100 if row.get('commission_rate', 0) > 1 else row.get('commission_rate', 0),
                        sales_volume=row.get('sales_volume', 100),  # 默认销量100
                        return_quantity=row.get('return_quantity', 10),  # 默认退货10
                        deal_orders=row.get('deal_orders', 95),  # 默认成交订单95
                        net_deal_orders=row.get('net_deal_orders', 85),  # 默认净成交订单85
                        post_shipping_refund_ratio=0.0,
                        ad_deal_price=row.get('ad_deal_price', 0),
                        ad_enabled=row.get('ad_enabled', False)
                    )
                    result = calculate_profit(input_data, order_count)
                    results.append(result)
                
                results_df = pd.DataFrame(results)
                st.write("📊 批量分析结果:")
                st.dataframe(results_df)
                
                fig = px.bar(
                    results_df.reset_index(),
                    x='index',
                    y='总利润',
                    title='各商品利润对比'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("请上传包含商品信息的CSV文件")
            st.write("CSV文件应包含以下列：")
            st.write("- model_name: 商品型号（可选）")
            st.write("- price: 商品售价")
            st.write("- cost: 商品成本")
            st.write("- other_cost: 其他成本")
            st.write("- shipping_fee: 运费")
            st.write("- commission_rate: 平台扣点（如3表示3%）")
            st.write("- sales_volume: 销量（可选，默认100）")
            st.write("- return_quantity: 退货数量（可选，默认10）")
            st.write("- deal_orders: 成交订单数（可选，默认95）")
            st.write("- net_deal_orders: 净成交订单数（可选，默认85）")
            st.write("- ad_deal_price: 每笔成交的广告费用（可选）")
            st.write("- ad_enabled: 是否启用广告 (True/False)（可选）")
    
    elif mode == "利润趋势分析":
        st.header("📈 利润趋势分析")
        
        user_input = collect_streamlit_input()
        
        col1, col2 = st.columns(2)
        with col1:
            price_min = st.number_input("最低售价", min_value=0.0, value=user_input.price * 0.8)
            price_max = st.number_input("最高售价", min_value=0.0, value=user_input.price * 1.5)
        
        with col2:
            price_step = st.number_input("价格步长", min_value=0.01, value=1.0)
        
        if st.button("📊 生成趋势图"):
            prices = []
            profits = []
            
            current_price = price_min
            while current_price <= price_max:
                # 创建新的输入对象，避免修改原始对象
                from src.input_module import ProfitInput
                test_input = ProfitInput(
                    model_name=user_input.model_name,
                    price=current_price,  # 使用当前测试价格
                    cost=user_input.cost,
                    other_cost=user_input.other_cost,
                    shipping_fee=user_input.shipping_fee,
                    commission_rate=user_input.commission_rate,
                    sales_volume=user_input.sales_volume,
                    return_quantity=user_input.return_quantity,
                    deal_orders=user_input.deal_orders,
                    net_deal_orders=user_input.net_deal_orders,
                    post_shipping_refund_ratio=user_input.post_shipping_refund_ratio,
                    ad_deal_price=user_input.ad_deal_price,
                    ad_enabled=user_input.ad_enabled
                )
                
                result = calculate_profit(test_input, order_count)
                
                prices.append(current_price)
                profits.append(result['总利润'])
                current_price += price_step
            
            fig = create_profit_trend_chart(prices, profits)
            st.plotly_chart(fig, use_container_width=True)
            
            trend_df = pd.DataFrame({
                '售价': prices,
                '利润': profits
            })
            st.write("📊 趋势数据:")
            st.dataframe(trend_df)
    
    elif mode == "历史数据管理":
        show_history_management()
    
    st.markdown("---")
    st.markdown("### 💡 使用说明")
    st.markdown("""
    1. **单品利润分析**: 分析单个商品的利润情况
    2. **批量分析**: 上传CSV文件批量分析多个商品
    3. **利润趋势分析**: 查看不同售价下的利润变化趋势
    4. **历史数据管理**: 查看和管理历史分析记录
    
    ### 💡 成交出价模式说明
    - 广告采用成交出价模式，只有在实际成交时才产生广告费用
    - 每笔成交订单会产生设定的广告费用
    - 系统会自动计算保本广告费用，帮助您优化广告策略
    """)

def show_history_management():
    """显示历史数据管理界面"""
    st.header("📚 历史数据管理")
    
    # 获取历史记录摘要
    summary = history_manager.get_history_summary()
    
    if summary['total_count'] == 0:
        st.info("📭 暂无历史记录")
        return
    
    # 显示摘要信息
    st.subheader("📊 历史记录摘要")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总记录数", summary['total_count'])
    
    with col2:
        if summary['date_range']:
            date_range = summary['date_range']
            st.metric("数据时间范围", f"{date_range['earliest'][:10]} ~ {date_range['latest'][:10]}")
    
    with col3:
        if summary['latest_analysis']:
            latest = summary['latest_analysis']
            st.metric("最新分析利润", f"{latest['result']['总利润']:.2f}元")
    
    # 功能选项卡
    tab1, tab2, tab3, tab4 = st.tabs(["📋 查看记录", "🔍 搜索记录", "📊 利润趋势", "🛠️ 管理操作"])
    
    with tab1:
        show_history_records()
    
    with tab2:
        search_history_records_ui()
    
    with tab3:
        show_profit_trend_ui()
    
    with tab4:
        show_management_operations()

def show_history_records():
    """显示历史记录列表"""
    st.subheader("📋 历史分析记录")
    
    history = history_manager.load_history()
    
    if not history:
        st.info("📭 暂无历史记录")
        return
    
    # 显示最近记录
    display_count = min(20, len(history))
    recent_records = history[-display_count:]
    recent_records.reverse()  # 最新的在前
    
    # 准备显示数据
    display_data = []
    for record in recent_records:
        result = record['result']
        display_data.append({
            '分析ID': record['analysis_id'],
            '时间': record['timestamp'][:19].replace('T', ' '),
            '商品型号': result.get('商品型号', 'N/A'),
            '售价': f"{record['input_data']['price']:.2f}元",
            '利润': f"{result['总利润']:.2f}元",
            '利润率': f"{result['利润率']:.2f}%",
            '广告启用': '是' if result.get('广告启用', False) else '否'
        })
    
    df = pd.DataFrame(display_data)
    
    # 可选择的记录
    selected_indices = st.multiselect(
        "选择要查看详情的记录（可多选）:",
        options=range(len(df)),
        format_func=lambda x: f"{df.iloc[x]['分析ID']} - {df.iloc[x]['商品型号']}"
    )
    
    st.dataframe(df, use_container_width=True)
    
    # 显示选中记录的详情
    if selected_indices:
        st.subheader("📝 记录详情")
        for idx in selected_indices:
            record = recent_records[idx]
            with st.expander(f"详情: {record['analysis_id']} - {record['result'].get('商品型号', 'N/A')}"):
                show_record_detail(record)

def show_record_detail(record):
    """显示单个记录的详细信息"""
    result = record['result']
    input_data = record['input_data']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**输入参数:**")
        st.write(f"- 商品型号: {input_data.get('model_name', 'N/A')}")
        st.write(f"- 商品售价: {input_data['price']:.2f}元")
        st.write(f"- 商品成本: {input_data['cost']:.2f}元")
        st.write(f"- 其他成本: {input_data['other_cost']:.2f}元")
        st.write(f"- 运费: {input_data['shipping_fee']:.2f}元")
        st.write(f"- 平台扣点: {input_data['commission_rate']*100:.1f}%")
        st.write(f"- 销量: {input_data['sales_volume']}")
        st.write(f"- 退货数量: {input_data['return_quantity']}")
        st.write(f"- 成交订单: {input_data['deal_orders']}")
        st.write(f"- 净成交订单: {input_data['net_deal_orders']}")
        if input_data.get('ad_enabled', False):
            st.write(f"- 广告出价: {input_data['ad_deal_price']:.2f}元/单")
    
    with col2:
        st.write("**计算结果:**")
        st.write(f"- 总利润: {result['总利润']:.2f}元")
        st.write(f"- 利润率: {result['利润率']:.2f}%")
        st.write(f"- 总收入: {result['总收入']:.2f}元")
        st.write(f"- 总成本: {result['总成本']:.2f}元")
        st.write(f"- 退款率: {result['退款率']:.2f}%")
        st.write(f"- 秒退率: {result['秒退率']:.2f}%")
        st.write(f"- 保本售价: {result['保本售价']:.2f}元")
        if result.get('广告启用', False):
            st.write(f"- 广告费用: {result['广告费用']:.2f}元")
            if result.get('保本广告出价') is not None:
                st.write(f"- 保本广告出价: {result['保本广告出价']:.2f}元/单")

def search_history_records_ui():
    """搜索历史记录界面"""
    st.subheader("🔍 搜索历史记录")
    
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            model_name = st.text_input("商品型号（模糊搜索）")
            min_profit = st.number_input("最小利润", value=None, step=0.01)
        
        with col2:
            max_profit = st.number_input("最大利润", value=None, step=0.01)
            date_range = st.date_input("分析日期范围", value=[])
        
        submitted = st.form_submit_button("🔍 搜索")
        
        if submitted:
            # 构建搜索条件
            filters = {}
            if model_name:
                filters['model_name'] = model_name
            if min_profit is not None:
                filters['min_profit'] = min_profit
            if max_profit is not None:
                filters['max_profit'] = max_profit
            
            results = history_manager.search_history(**filters)
            
            if not results:
                st.info("📭 未找到匹配的记录")
            else:
                st.success(f"✅ 找到 {len(results)} 条匹配记录")
                
                # 显示搜索结果
                display_data = []
                for record in results:
                    result = record['result']
                    display_data.append({
                        '分析ID': record['analysis_id'],
                        '时间': record['timestamp'][:19].replace('T', ' '),
                        '商品型号': result.get('商品型号', 'N/A'),
                        '利润': f"{result['总利润']:.2f}元",
                        '利润率': f"{result['利润率']:.2f}%"
                    })
                
                df = pd.DataFrame(display_data)
                st.dataframe(df, use_container_width=True)

def show_profit_trend_ui():
    """显示利润趋势界面"""
    st.subheader("📊 利润趋势分析")
    
    trend_data = history_manager.get_profit_trend()
    
    if "message" in trend_data:
        st.info(f"📈 {trend_data['message']}")
        return
    
    # 显示趋势摘要
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("趋势方向", trend_data['trend_direction'])
    
    with col2:
        st.metric("平均利润", f"{trend_data['avg_profit']:.2f}元")
    
    with col3:
        st.metric("分析记录数", len(trend_data['profits']))
    
    # 绘制趋势图
    if len(trend_data['dates']) > 1:
        trend_df = pd.DataFrame({
            '日期': trend_data['dates'],
            '利润': trend_data['profits'],
            '商品型号': trend_data['models']
        })
        
        fig = px.line(
            trend_df,
            x='日期',
            y='利润',
            title='利润变化趋势',
            hover_data=['商品型号']
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 显示详细数据
        st.subheader("📋 趋势数据")
        st.dataframe(trend_df, use_container_width=True)

def show_management_operations():
    """显示管理操作界面"""
    st.subheader("🛠️ 管理操作")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**导出操作**")
        if st.button("📥 导出历史记录到Excel", type="primary"):
            try:
                filename = history_manager.export_history_to_excel()
                st.success(f"✅ 历史记录已导出到: {filename}")
            except ValueError as e:
                st.error(f"❌ 导出失败: {e}")
            except Exception as e:
                st.error(f"❌ 导出过程中发生错误: {e}")
    
    with col2:
        st.write("**删除操作**")
        
        # 删除特定记录
        analysis_id = st.text_input("输入要删除的分析ID")
        if st.button("🗑️ 删除指定记录", type="secondary"):
            if analysis_id:
                if history_manager.delete_analysis(analysis_id):
                    st.success("✅ 记录已删除")
                    st.rerun()
                else:
                    st.error("❌ 未找到指定的分析记录或删除失败")
            else:
                st.warning("请输入分析ID")
        
        # 清空所有记录
        st.write("**危险操作**")
        
        summary = history_manager.get_history_summary()
        if summary['total_count'] > 0:
            st.warning(f"⚠️ 即将删除所有 {summary['total_count']} 条历史记录")
            
            # 使用表单来处理确认输入和清空操作
            with st.form("clear_history_form"):
                confirm_text = st.text_input("请输入 'DELETE' 确认清空所有记录")
                clear_button = st.form_submit_button("🗑️ 确认清空所有历史记录", type="secondary")
                
                if clear_button:
                    if confirm_text == 'DELETE':
                        if history_manager.clear_history():
                            st.success("✅ 所有历史记录已清空")
                            st.rerun()
                        else:
                            st.error("❌ 清空失败")
                    elif confirm_text:
                        st.error("❌ 请输入 'DELETE' 确认")
                    else:
                        st.error("❌ 请输入确认文本")
        else:
            st.info("📭 暂无历史记录")

if __name__ == "__main__":
    main()