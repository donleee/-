#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多利润分析系统 - GUI界面
支持Windows和Mac系统的独立应用
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

from src.input_module import ProfitInput
from src.calculation_engine import calculate_profit
from src.history_manager import history_manager
from src.output_module import export_to_excel


class ProfitAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("拼多多利润分析系统 v1.0")
        self.root.geometry("1200x800")
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # 创建主界面
        self.create_widgets()
        
    def create_widgets(self):
        # 创建笔记本控件（选项卡）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建各个选项卡
        self.create_analysis_tab()
        self.create_batch_tab()
        self.create_history_tab()
        self.create_trend_tab()
        
    def create_analysis_tab(self):
        """创建单品分析选项卡"""
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="单品利润分析")
        
        # 左侧输入区域
        input_frame = ttk.LabelFrame(self.analysis_frame, text="输入参数", padding=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 输入字段
        fields = [
            ("商品型号", "model_name", ""),
            ("商品售价", "price", "100.0"),
            ("商品成本", "cost", "50.0"),
            ("其他成本", "other_cost", "5.0"),
            ("运费", "shipping_fee", "10.0"),
            ("平台扣点(%)", "commission_rate", "3"),
            ("销量", "sales_volume", "100"),
            ("退货数量", "return_quantity", "10"),
            ("成交订单数", "deal_orders", "95"),
            ("净成交订单数", "net_deal_orders", "85"),
            ("广告出价", "ad_deal_price", "2.0"),
            ("分析订单数", "order_count", "100"),
        ]
        
        self.entries = {}
        for i, (label, key, default) in enumerate(fields):
            ttk.Label(input_frame, text=label + ":").grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(input_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=(10, 0), pady=2)
            self.entries[key] = entry
        
        # 广告启用复选框
        self.ad_enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="启用广告", variable=self.ad_enabled_var).grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # 计算按钮
        ttk.Button(input_frame, text="计算利润", command=self.calculate_profit).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        # 右侧结果区域
        result_frame = ttk.LabelFrame(self.analysis_frame, text="分析结果", padding=10)
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 结果显示文本框
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮框架
        button_frame = ttk.Frame(result_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="导出Excel", command=self.export_excel).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="清空结果", command=self.clear_result).pack(side=tk.LEFT)
        
    def create_batch_tab(self):
        """创建批量分析选项卡"""
        self.batch_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.batch_frame, text="批量分析")
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(self.batch_frame, text="文件选择", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=60).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="选择CSV文件", command=self.select_csv_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="批量计算", command=self.batch_calculate).pack(side=tk.LEFT)
        
        # 结果显示区域
        self.batch_tree = ttk.Treeview(self.batch_frame, columns=("型号", "售价", "利润", "利润率", "退款率"), show="headings")
        self.batch_tree.heading("型号", text="商品型号")
        self.batch_tree.heading("售价", text="售价")
        self.batch_tree.heading("利润", text="总利润")
        self.batch_tree.heading("利润率", text="利润率(%)")
        self.batch_tree.heading("退款率", text="退款率(%)")
        
        self.batch_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_history_tab(self):
        """创建历史记录选项卡"""
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="历史记录")
        
        # 控制按钮区域
        control_frame = ttk.Frame(self.history_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="刷新", command=self.refresh_history).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="导出历史", command=self.export_history).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="清空历史", command=self.clear_history).pack(side=tk.LEFT, padx=(0, 10))
        
        # 搜索区域
        search_frame = ttk.LabelFrame(self.history_frame, text="搜索", padding=5)
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(search_frame, text="型号:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_model = ttk.Entry(search_frame, width=20)
        self.search_model.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(search_frame, text="最小利润:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_min_profit = ttk.Entry(search_frame, width=15)
        self.search_min_profit.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(search_frame, text="搜索", command=self.search_history).pack(side=tk.LEFT)
        
        # 历史记录列表
        self.history_tree = ttk.Treeview(self.history_frame, columns=("ID", "时间", "型号", "利润", "利润率"), show="headings")
        self.history_tree.heading("ID", text="分析ID")
        self.history_tree.heading("时间", text="创建时间")
        self.history_tree.heading("型号", text="商品型号")
        self.history_tree.heading("利润", text="总利润")
        self.history_tree.heading("利润率", text="利润率(%)")
        
        # 设置列宽
        self.history_tree.column("ID", width=150)
        self.history_tree.column("时间", width=150)
        self.history_tree.column("型号", width=120)
        self.history_tree.column("利润", width=100)
        self.history_tree.column("利润率", width=100)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 绑定双击事件
        self.history_tree.bind("<Double-1>", self.show_history_detail)
        
    def create_trend_tab(self):
        """创建趋势分析选项卡"""
        self.trend_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trend_frame, text="趋势分析")
        
        # 参数设置区域
        param_frame = ttk.LabelFrame(self.trend_frame, text="趋势参数", padding=10)
        param_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 趋势参数输入
        ttk.Label(param_frame, text="最低价格:").grid(row=0, column=0, padx=(0, 5))
        self.trend_min_price = ttk.Entry(param_frame, width=10)
        self.trend_min_price.insert(0, "80")
        self.trend_min_price.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(param_frame, text="最高价格:").grid(row=0, column=2, padx=(0, 5))
        self.trend_max_price = ttk.Entry(param_frame, width=10)
        self.trend_max_price.insert(0, "150")
        self.trend_max_price.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(param_frame, text="价格步长:").grid(row=0, column=4, padx=(0, 5))
        self.trend_step = ttk.Entry(param_frame, width=10)
        self.trend_step.insert(0, "5")
        self.trend_step.grid(row=0, column=5, padx=(0, 10))
        
        ttk.Button(param_frame, text="生成趋势图", command=self.generate_trend).grid(row=0, column=6, padx=(10, 0))
        
        # 图表显示区域
        self.trend_canvas_frame = ttk.Frame(self.trend_frame)
        self.trend_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def calculate_profit(self):
        """计算利润"""
        try:
            # 获取输入数据
            input_data = ProfitInput(
                model_name=self.entries['model_name'].get() or "未命名商品",
                price=float(self.entries['price'].get()),
                cost=float(self.entries['cost'].get()),
                other_cost=float(self.entries['other_cost'].get()),
                shipping_fee=float(self.entries['shipping_fee'].get()),
                commission_rate=float(self.entries['commission_rate'].get()) / 100,
                sales_volume=int(self.entries['sales_volume'].get()),
                return_quantity=int(self.entries['return_quantity'].get()),
                deal_orders=int(self.entries['deal_orders'].get()),
                net_deal_orders=int(self.entries['net_deal_orders'].get()),
                post_shipping_refund_ratio=0.0,
                ad_deal_price=float(self.entries['ad_deal_price'].get()),
                ad_enabled=self.ad_enabled_var.get()
            )
            
            order_count = int(self.entries['order_count'].get())
            
            # 计算结果
            result = calculate_profit(input_data, order_count)
            
            # 显示结果
            self.display_result(result)
            
            # 保存到历史记录
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
                'analysis_orders': order_count
            }
            
            analysis_id = history_manager.save_analysis(input_dict, result)
            
            # 存储当前结果用于导出
            self.current_result = result
            
            messagebox.showinfo("成功", f"计算完成！已保存到历史记录，ID: {analysis_id}")
            
        except ValueError as e:
            messagebox.showerror("输入错误", "请检查输入的数值是否正确")
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中发生错误: {str(e)}")
    
    def display_result(self, result):
        """显示计算结果"""
        self.result_text.delete(1.0, tk.END)
        
        output = f"""
╔══════════════════════════════════════════════════════════════╗
║                     拼多多利润分析报告                        ║
╚══════════════════════════════════════════════════════════════╝

🏷️  商品型号: {result.get('商品型号', 'N/A')}

📊 利润分析:
  • 总利润: {result['总利润']:.2f} 元
  • 单均利润: {result['单均利润']:.2f} 元
  • 利润率: {result['利润率']:.2f}%
  • 总收入: {result['总收入']:.2f} 元
  • 总成本: {result['总成本']:.2f} 元

📦 订单数据:
  • 分析订单数: {result['订单总数']}
  • 销量: {result['销量']}
  • 退货数量: {result['退货数量']}
  • 成交订单数: {result['成交订单数']}
  • 净成交订单数: {result['净成交订单数']}
  • 退款率: {result['退款率']:.2f}%
  • 秒退率: {result['秒退率']:.2f}%

💰 成本构成:"""
        
        for item, cost in result['成本构成'].items():
            output += f"\n  • {item}: {cost:.2f} 元"
        
        output += f"""

🎯 保本分析:
  • 保本售价: {result['保本售价']:.2f} 元
"""
        
        if result.get('广告启用', False):
            output += f"""  • 广告费用: {result['广告费用']:.2f} 元
  • 保本广告出价: {result['保本广告出价']:.2f} 元
  • 最高广告投入: {result['最高广告投入']:.2f} 元
  • 当前ROI: {result['当前ROI']:.2f}
  • 保本ROI: {result['保本ROI']:.2f}"""
        
        self.result_text.insert(tk.END, output)
    
    def export_excel(self):
        """导出Excel"""
        if not hasattr(self, 'current_result'):
            messagebox.showwarning("提示", "请先进行利润计算")
            return
        
        try:
            filename = export_to_excel(self.current_result)
            messagebox.showinfo("导出成功", f"Excel报告已导出: {filename}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出过程中发生错误: {str(e)}")
    
    def clear_result(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        if hasattr(self, 'current_result'):
            delattr(self, 'current_result')
    
    def select_csv_file(self):
        """选择CSV文件"""
        filename = filedialog.askopenfilename(
            title="选择CSV文件",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def batch_calculate(self):
        """批量计算"""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showwarning("提示", "请先选择CSV文件")
            return
        
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 清空现有结果
            for item in self.batch_tree.get_children():
                self.batch_tree.delete(item)
            
            # 批量计算
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
                
                # 添加到表格
                self.batch_tree.insert("", tk.END, values=(
                    result['商品型号'],
                    f"{input_data.price:.2f}",
                    f"{result['总利润']:.2f}",
                    f"{result['利润率']:.2f}",
                    f"{result['退款率']:.2f}"
                ))
            
            messagebox.showinfo("成功", f"批量计算完成，处理了 {len(df)} 条记录")
            
        except Exception as e:
            messagebox.showerror("批量计算失败", f"处理过程中发生错误: {str(e)}")
    
    def refresh_history(self):
        """刷新历史记录"""
        # 清空现有记录
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 加载历史记录
        history = history_manager.load_history()
        
        # 显示最近的记录
        for record in reversed(history[-50:]):  # 显示最近50条
            result = record['result']
            self.history_tree.insert("", tk.END, values=(
                record['analysis_id'],
                record['timestamp'][:19].replace('T', ' '),
                result.get('商品型号', 'N/A'),
                f"{result['总利润']:.2f}",
                f"{result['利润率']:.2f}"
            ))
    
    def search_history(self):
        """搜索历史记录"""
        model_name = self.search_model.get().strip()
        min_profit_str = self.search_min_profit.get().strip()
        
        filters = {}
        if model_name:
            filters['model_name'] = model_name
        if min_profit_str:
            try:
                filters['min_profit'] = float(min_profit_str)
            except ValueError:
                messagebox.showerror("输入错误", "最小利润必须是数字")
                return
        
        # 搜索
        results = history_manager.search_history(**filters)
        
        # 清空现有记录
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # 显示搜索结果
        for record in results:
            result = record['result']
            self.history_tree.insert("", tk.END, values=(
                record['analysis_id'],
                record['timestamp'][:19].replace('T', ' '),
                result.get('商品型号', 'N/A'),
                f"{result['总利润']:.2f}",
                f"{result['利润率']:.2f}"
            ))
        
        messagebox.showinfo("搜索完成", f"找到 {len(results)} 条匹配记录")
    
    def show_history_detail(self, event):
        """显示历史记录详情"""
        selection = self.history_tree.selection()
        if not selection:
            return
        
        item = self.history_tree.item(selection[0])
        analysis_id = item['values'][0]
        
        # 查找记录
        history = history_manager.load_history()
        record = None
        for r in history:
            if r['analysis_id'] == analysis_id:
                record = r
                break
        
        if record:
            # 显示详情窗口
            self.show_detail_window(record)
    
    def show_detail_window(self, record):
        """显示详情窗口"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"详情 - {record['analysis_id']}")
        detail_window.geometry("600x500")
        
        # 创建文本框
        text_widget = tk.Text(detail_window, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(detail_window, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # 显示详细信息
        result = record['result']
        input_data = record['input_data']
        
        detail_text = f"""
分析ID: {record['analysis_id']}
创建时间: {record['timestamp']}

输入参数:
  • 商品型号: {input_data.get('model_name', 'N/A')}
  • 商品售价: {input_data['price']:.2f} 元
  • 商品成本: {input_data['cost']:.2f} 元
  • 其他成本: {input_data['other_cost']:.2f} 元
  • 运费: {input_data['shipping_fee']:.2f} 元
  • 平台扣点: {input_data['commission_rate']*100:.1f}%
  • 销量: {input_data['sales_volume']}
  • 退货数量: {input_data['return_quantity']}
  • 成交订单: {input_data['deal_orders']}
  • 净成交订单: {input_data['net_deal_orders']}
  • 广告出价: {input_data['ad_deal_price']:.2f} 元
  • 广告启用: {'是' if input_data.get('ad_enabled', False) else '否'}

计算结果:
  • 总利润: {result['总利润']:.2f} 元
  • 利润率: {result['利润率']:.2f}%
  • 总收入: {result['总收入']:.2f} 元
  • 总成本: {result['总成本']:.2f} 元
  • 退款率: {result['退款率']:.2f}%
  • 秒退率: {result['秒退率']:.2f}%
  • 保本售价: {result['保本售价']:.2f} 元
"""
        
        if result.get('广告启用', False):
            detail_text += f"""  • 广告费用: {result['广告费用']:.2f} 元
  • 保本广告出价: {result['保本广告出价']:.2f} 元
"""
        
        text_widget.insert(tk.END, detail_text)
        text_widget.configure(state='disabled')
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def export_history(self):
        """导出历史记录"""
        try:
            filename = history_manager.export_history_to_excel()
            messagebox.showinfo("导出成功", f"历史记录已导出: {filename}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出过程中发生错误: {str(e)}")
    
    def clear_history(self):
        """清空历史记录"""
        result = messagebox.askyesno("确认清空", "确定要清空所有历史记录吗？此操作不可恢复！")
        if result:
            confirm = messagebox.askstring("二次确认", "请输入 'DELETE' 确认清空操作:")
            if confirm == 'DELETE':
                if history_manager.clear_history():
                    messagebox.showinfo("成功", "所有历史记录已清空")
                    self.refresh_history()
                else:
                    messagebox.showerror("失败", "清空失败")
    
    def generate_trend(self):
        """生成趋势图"""
        try:
            min_price = float(self.trend_min_price.get())
            max_price = float(self.trend_max_price.get())
            step = float(self.trend_step.get())
            
            if min_price >= max_price:
                messagebox.showerror("参数错误", "最低价格必须小于最高价格")
                return
            
            # 获取基础参数（使用单品分析的参数）
            base_input = ProfitInput(
                model_name="趋势分析",
                price=100.0,  # 这个会被替换
                cost=float(self.entries['cost'].get()),
                other_cost=float(self.entries['other_cost'].get()),
                shipping_fee=float(self.entries['shipping_fee'].get()),
                commission_rate=float(self.entries['commission_rate'].get()) / 100,
                sales_volume=int(self.entries['sales_volume'].get()),
                return_quantity=int(self.entries['return_quantity'].get()),
                deal_orders=int(self.entries['deal_orders'].get()),
                net_deal_orders=int(self.entries['net_deal_orders'].get()),
                post_shipping_refund_ratio=0.0,
                ad_deal_price=float(self.entries['ad_deal_price'].get()),
                ad_enabled=self.ad_enabled_var.get()
            )
            
            # 计算趋势数据
            prices = []
            profits = []
            
            current_price = min_price
            while current_price <= max_price:
                test_input = ProfitInput(
                    model_name=base_input.model_name,
                    price=current_price,
                    cost=base_input.cost,
                    other_cost=base_input.other_cost,
                    shipping_fee=base_input.shipping_fee,
                    commission_rate=base_input.commission_rate,
                    sales_volume=base_input.sales_volume,
                    return_quantity=base_input.return_quantity,
                    deal_orders=base_input.deal_orders,
                    net_deal_orders=base_input.net_deal_orders,
                    post_shipping_refund_ratio=base_input.post_shipping_refund_ratio,
                    ad_deal_price=base_input.ad_deal_price,
                    ad_enabled=base_input.ad_enabled
                )
                
                result = calculate_profit(test_input, int(self.entries['order_count'].get()))
                prices.append(current_price)
                profits.append(result['总利润'])
                current_price += step
            
            # 绘制图表
            self.plot_trend(prices, profits)
            
        except ValueError:
            messagebox.showerror("输入错误", "请检查趋势参数输入是否正确")
        except Exception as e:
            messagebox.showerror("生成失败", f"生成趋势图时发生错误: {str(e)}")
    
    def plot_trend(self, prices, profits):
        """绘制趋势图"""
        # 清除之前的图表
        for widget in self.trend_canvas_frame.winfo_children():
            widget.destroy()
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(prices, profits, marker='o', linewidth=2, markersize=4)
        ax.set_xlabel('售价 (元)')
        ax.set_ylabel('利润 (元)')
        ax.set_title('不同售价下的利润变化趋势')
        ax.grid(True, alpha=0.3)
        
        # 添加到GUI
        canvas = FigureCanvasTkAgg(fig, self.trend_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.tight_layout()


def main():
    """主函数"""
    root = tk.Tk()
    app = ProfitAnalysisGUI(root)
    
    # 加载历史记录
    app.refresh_history()
    
    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    main()