#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多利润分析系统 - 简化GUI版本
适用于可能存在tkinter兼容性问题的环境
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("警告: tkinter不可用，将使用命令行界面")

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.input_module import ProfitInput, collect_user_input
from src.calculation_engine import calculate_profit
from src.output_module import print_profit_report, export_to_excel
from src.history_manager import history_manager


class SimpleGUI:
    """简化的GUI界面"""
    
    def __init__(self):
        if not TKINTER_AVAILABLE:
            self.run_cli()
            return
            
        try:
            self.root = tk.Tk()
            self.root.title("拼多多利润分析系统")
            self.root.geometry("800x600")
            self.create_simple_interface()
        except Exception as e:
            print(f"GUI初始化失败: {e}")
            print("切换到命令行模式...")
            self.run_cli()
    
    def create_simple_interface(self):
        """创建简化界面"""
        # 主标题
        title_label = tk.Label(self.root, text="拼多多利润分析系统", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 功能按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # 功能按钮
        tk.Button(button_frame, text="单品利润分析", 
                 command=self.single_analysis, width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="批量分析", 
                 command=self.batch_analysis, width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="历史记录", 
                 command=self.view_history, width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="命令行模式", 
                 command=self.run_cli_mode, width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(self.root, text="分析结果", font=("Arial", 12))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 底部按钮
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        
        tk.Button(bottom_frame, text="导出Excel", command=self.export_excel).pack(side=tk.LEFT)
        tk.Button(bottom_frame, text="清空结果", command=self.clear_result).pack(side=tk.LEFT, padx=10)
        tk.Button(bottom_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT)
    
    def single_analysis(self):
        """单品分析"""
        try:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "请在命令行中输入商品信息...\n")
            self.root.update()
            
            # 使用命令行输入
            print("\n=== 单品利润分析 ===")
            input_data = collect_user_input()
            result = calculate_profit(input_data, 100)
            
            # 保存结果
            self.current_result = result
            
            # 显示结果
            self.display_result(result)
            
            # 保存历史记录
            input_dict = {
                'model_name': input_data.model_name,
                'price': input_data.price,
                'cost': input_data.cost,
                'other_cost': input_data.other_cost,
                'shipping_fee': input_data.shipping_fee,
                'commission_rate': input_data.commission_rate,
                'sales_volume': input_data.sales_volume,
                'return_quantity': input_data.return_quantity,
                'deal_orders': input_data.deal_orders,
                'net_deal_orders': input_data.net_deal_orders,
                'ad_deal_price': input_data.ad_deal_price,
                'ad_enabled': input_data.ad_enabled,
                'analysis_orders': 100
            }
            
            analysis_id = history_manager.save_analysis(input_dict, result)
            messagebox.showinfo("成功", f"分析完成！已保存，ID: {analysis_id}")
            
        except Exception as e:
            messagebox.showerror("错误", f"分析失败: {e}")
    
    def batch_analysis(self):
        """批量分析"""
        try:
            filename = filedialog.askopenfilename(
                title="选择CSV文件",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            import pandas as pd
            
            df = pd.read_csv(filename)
            results = []
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"正在处理 {len(df)} 条记录...\n")
            self.root.update()
            
            for idx, row in df.iterrows():
                input_data = ProfitInput(
                    model_name=row.get('model_name', f'SKU-{idx}'),
                    price=row.get('price', 0),
                    cost=row.get('cost', 0),
                    other_cost=row.get('other_cost', 0),
                    shipping_fee=row.get('shipping_fee', 0),
                    commission_rate=row.get('commission_rate', 0) / 100 if row.get('commission_rate', 0) > 1 else row.get('commission_rate', 0),
                    sales_volume=row.get('sales_volume', 100),
                    return_quantity=row.get('return_quantity', 10),
                    deal_orders=row.get('deal_orders', 95),
                    net_deal_orders=row.get('net_deal_orders', 85),
                    post_shipping_refund_ratio=0.0,
                    ad_deal_price=row.get('ad_deal_price', 0),
                    ad_enabled=row.get('ad_enabled', False)
                )
                
                result = calculate_profit(input_data, 100)
                results.append(result)
                
                self.result_text.insert(tk.END, f"{input_data.model_name}: {result['总利润']:.2f}元\n")
                self.root.update()
            
            messagebox.showinfo("成功", f"批量分析完成！处理了 {len(results)} 条记录")
            
        except Exception as e:
            messagebox.showerror("错误", f"批量分析失败: {e}")
    
    def view_history(self):
        """查看历史记录"""
        try:
            summary = history_manager.get_history_summary()
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"历史记录摘要\n")
            self.result_text.insert(tk.END, f"{'='*30}\n")
            self.result_text.insert(tk.END, f"总记录数: {summary['total_count']}\n")
            
            if summary['total_count'] > 0:
                history = history_manager.load_history()
                self.result_text.insert(tk.END, f"\n最近记录:\n")
                
                for record in reversed(history[-10:]):
                    result = record['result']
                    self.result_text.insert(tk.END, 
                        f"{record['analysis_id']}: {result['商品型号']} - {result['总利润']:.2f}元\n")
            
        except Exception as e:
            messagebox.showerror("错误", f"查看历史失败: {e}")
    
    def display_result(self, result):
        """显示结果"""
        self.result_text.delete(1.0, tk.END)
        
        output = f"""拼多多利润分析报告
{'='*40}

商品型号: {result.get('商品型号', 'N/A')}

💰 利润分析:
  总利润: {result['总利润']:.2f} 元
  单均利润: {result['单均利润']:.2f} 元
  利润率: {result['利润率']:.2f}%
  总收入: {result['总收入']:.2f} 元
  总成本: {result['总成本']:.2f} 元

📦 订单数据:
  销量: {result['销量']}
  退货数量: {result['退货数量']}
  成交订单: {result['成交订单数']}
  净成交订单: {result['净成交订单数']}
  退款率: {result['退款率']:.2f}%
  秒退率: {result['秒退率']:.2f}%

💰 成本构成:"""
        
        for item, cost in result['成本构成'].items():
            output += f"\n  {item}: {cost:.2f} 元"
        
        output += f"\n\n🎯 保本分析:\n  保本售价: {result['保本售价']:.2f} 元"
        
        if result.get('广告启用', False):
            output += f"\n  广告费用: {result['广告费用']:.2f} 元"
            output += f"\n  保本广告出价: {result['保本广告出价']:.2f} 元"
        
        self.result_text.insert(tk.END, output)
    
    def export_excel(self):
        """导出Excel"""
        if hasattr(self, 'current_result'):
            try:
                filename = export_to_excel(self.current_result)
                messagebox.showinfo("成功", f"已导出: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
        else:
            messagebox.showwarning("提示", "请先进行分析")
    
    def clear_result(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        if hasattr(self, 'current_result'):
            delattr(self, 'current_result')
    
    def run_cli_mode(self):
        """运行命令行模式"""
        print("\n切换到命令行模式...")
        self.root.withdraw()  # 隐藏GUI窗口
        self.run_cli()
        self.root.deiconify()  # 恢复GUI窗口
    
    def run_cli(self):
        """运行命令行界面"""
        from main import main as cli_main
        cli_main()
    
    def run(self):
        """运行GUI"""
        if TKINTER_AVAILABLE and hasattr(self, 'root'):
            try:
                self.root.mainloop()
            except Exception as e:
                print(f"GUI运行出错: {e}")
                self.run_cli()
        else:
            self.run_cli()


def main():
    """主函数"""
    print("拼多多利润分析系统")
    print("=" * 30)
    
    if TKINTER_AVAILABLE:
        print("正在启动图形界面...")
        try:
            app = SimpleGUI()
            app.run()
        except Exception as e:
            print(f"图形界面启动失败: {e}")
            print("切换到命令行模式...")
            from main import main as cli_main
            cli_main()
    else:
        print("图形界面不可用，使用命令行模式...")
        from main import main as cli_main
        cli_main()


if __name__ == "__main__":
    main()