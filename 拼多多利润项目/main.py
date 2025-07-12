#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多利润项目 - 主程序
"""

import sys
import argparse
from src.input_module import collect_user_input
from src.calculation_engine import calculate_profit
from src.output_module import print_profit_report, plot_cost_breakdown
from src.history_manager import history_manager

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='拼多多利润分析系统')
    parser.add_argument('--mode', choices=['cli', 'web'], default='cli', 
                       help='运行模式: cli(命令行) 或 web(网页)')
    parser.add_argument('--orders', type=int, default=100, 
                       help='分析订单数量 (默认: 100)')
    parser.add_argument('--export', action='store_true',
                       help='导出Excel报告')
    parser.add_argument('--history', action='store_true',
                       help='查看历史记录')
    parser.add_argument('--save-history', action='store_true', default=True,
                       help='保存分析到历史记录 (默认: True)')
    
    args = parser.parse_args()
    
    if args.mode == 'web':
        print("启动Web界面...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'web_app.py'])
        return
    
    if args.history:
        show_history_menu()
        return
    
    print("=" * 50)
    print("💰 拼多多利润计算软件")
    print("=" * 50)
    print("欢迎使用拼多多利润分析系统！")
    print("这是一个用于分析和计算拼多多商品利润的项目。")
    print("-" * 50)
    
    try:
        user_input = collect_user_input()
        result = calculate_profit(user_input, args.orders)
        print_profit_report(result)
        
        # 保存到历史记录
        if args.save_history:
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
                'analysis_orders': args.orders
            }
            
            analysis_id = history_manager.save_analysis(input_dict, result)
            print(f"\n💾 分析已保存到历史记录，ID: {analysis_id}")
        
        if args.export:
            from src.output_module import export_to_excel
            filename = export_to_excel(result)
            print(f"\n📥 Excel报告已导出: {filename}")
        
        print("\n🎨 正在生成成本构成图表...")
        plot_cost_breakdown(result['成本构成'])
        
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("请检查输入数据是否正确")

def show_history_menu():
    """显示历史记录菜单"""
    while True:
        print("\n" + "=" * 50)
        print("📚 历史记录管理")
        print("=" * 50)
        print("1. 查看历史记录摘要")
        print("2. 查看所有历史记录")
        print("3. 搜索历史记录")
        print("4. 删除指定记录")
        print("5. 清空所有记录")
        print("6. 导出历史记录")
        print("7. 查看利润趋势")
        print("0. 返回主菜单")
        print("-" * 50)
        
        choice = input("请选择操作 (0-7): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            show_history_summary()
        elif choice == '2':
            show_all_history()
        elif choice == '3':
            search_history_records()
        elif choice == '4':
            delete_history_record()
        elif choice == '5':
            clear_all_history()
        elif choice == '6':
            export_history()
        elif choice == '7':
            show_profit_trend()
        else:
            print("❌ 无效选择，请重新输入")

def show_history_summary():
    """显示历史记录摘要"""
    summary = history_manager.get_history_summary()
    
    print(f"\n📊 历史记录摘要:")
    print(f"   总记录数: {summary['total_count']}")
    
    if summary['total_count'] > 0:
        date_range = summary['date_range']
        latest = summary['latest_analysis']
        
        print(f"   时间范围: {date_range['earliest'][:10]} ~ {date_range['latest'][:10]}")
        print(f"   最新分析: {latest['result']['商品型号']} (利润: {latest['result']['总利润']:.2f}元)")

def show_all_history():
    """显示所有历史记录"""
    history = history_manager.load_history()
    
    if not history:
        print("\n📭 暂无历史记录")
        return
    
    print(f"\n📋 历史记录列表 (共{len(history)}条):")
    print("-" * 80)
    print(f"{'ID':<15} {'时间':<12} {'商品型号':<15} {'利润':<10} {'利润率':<8}")
    print("-" * 80)
    
    for record in reversed(history[-10:]):  # 显示最近10条
        result = record['result']
        print(f"{record['analysis_id']:<15} {record['timestamp'][:10]:<12} "
              f"{result['商品型号']:<15} {result['总利润']:>8.2f} {result['利润率']:>6.2f}%")

def search_history_records():
    """搜索历史记录"""
    print("\n🔍 搜索历史记录")
    print("留空跳过该条件")
    
    model_name = input("商品型号 (模糊匹配): ").strip()
    
    try:
        min_profit = input("最小利润: ").strip()
        min_profit = float(min_profit) if min_profit else None
        
        max_profit = input("最大利润: ").strip()
        max_profit = float(max_profit) if max_profit else None
    except ValueError:
        print("❌ 利润必须是数字")
        return
    
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
        print("\n📭 未找到匹配的记录")
        return
    
    print(f"\n📋 搜索结果 (共{len(results)}条):")
    print("-" * 80)
    print(f"{'ID':<15} {'时间':<12} {'商品型号':<15} {'利润':<10} {'利润率':<8}")
    print("-" * 80)
    
    for record in results:
        result = record['result']
        print(f"{record['analysis_id']:<15} {record['timestamp'][:10]:<12} "
              f"{result['商品型号']:<15} {result['总利润']:>8.2f} {result['利润率']:>6.2f}%")

def delete_history_record():
    """删除历史记录"""
    analysis_id = input("请输入要删除的分析ID: ").strip()
    
    if not analysis_id:
        print("❌ 分析ID不能为空")
        return
    
    if history_manager.delete_analysis(analysis_id):
        print("✅ 记录已删除")
    else:
        print("❌ 未找到指定的分析记录或删除失败")

def clear_all_history():
    """清空所有历史记录"""
    summary = history_manager.get_history_summary()
    
    if summary['total_count'] == 0:
        print("\n📭 暂无历史记录")
        return
    
    print(f"\n⚠️  即将删除所有 {summary['total_count']} 条历史记录")
    confirm = input("确认清空所有历史记录？请输入 'DELETE' 确认: ").strip()
    
    if confirm == 'DELETE':
        if history_manager.clear_history():
            print("✅ 所有历史记录已清空")
        else:
            print("❌ 清空失败")
    else:
        print("❌ 取消清空")

def export_history():
    """导出历史记录"""
    try:
        filename = history_manager.export_history_to_excel()
        print(f"✅ 历史记录已导出到: {filename}")
    except ValueError as e:
        print(f"❌ 导出失败: {e}")
    except Exception as e:
        print(f"❌ 导出过程中发生错误: {e}")

def show_profit_trend():
    """显示利润趋势"""
    trend_data = history_manager.get_profit_trend()
    
    if "message" in trend_data:
        print(f"\n📈 {trend_data['message']}")
        return
    
    print(f"\n📈 利润趋势分析:")
    print(f"   趋势方向: {trend_data['trend_direction']}")
    print(f"   平均利润: {trend_data['avg_profit']:.2f}元")
    print(f"   分析期间: {trend_data['dates'][0]} ~ {trend_data['dates'][-1]}")
    
    print(f"\n📊 最近分析记录:")
    for i, (date, profit, model) in enumerate(zip(
        trend_data['dates'][-5:], 
        trend_data['profits'][-5:], 
        trend_data['models'][-5:]
    )):
        print(f"   {date}: {model} - {profit:.2f}元")

if __name__ == "__main__":
    main()
