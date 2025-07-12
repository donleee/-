import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, history_file: str = "data/analysis_history.json"):
        self.history_file = history_file
        self.ensure_data_dir()
        
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
    
    def save_analysis(self, input_data: dict, result: dict) -> str:
        """
        保存分析记录
        
        Args:
            input_data: 输入参数
            result: 计算结果
            
        Returns:
            analysis_id: 分析记录ID
        """
        analysis_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        record = {
            "analysis_id": analysis_id,
            "timestamp": datetime.now().isoformat(),
            "input_data": input_data,
            "result": result,
            "created_by": "user"
        }
        
        # 读取现有历史记录
        history = self.load_history()
        
        # 添加新记录
        history.append(record)
        
        # 保存到文件
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2, default=str)
        
        return analysis_id
    
    def load_history(self) -> List[Dict]:
        """加载历史记录"""
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict]:
        """获取指定的分析记录"""
        history = self.load_history()
        for record in history:
            if record.get('analysis_id') == analysis_id:
                return record
        return None
    
    def delete_analysis(self, analysis_id: str) -> bool:
        """删除指定的分析记录"""
        history = self.load_history()
        original_count = len(history)
        
        history = [record for record in history if record.get('analysis_id') != analysis_id]
        
        if len(history) < original_count:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2, default=str)
            return True
        return False
    
    def clear_history(self) -> bool:
        """清空所有历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return True
        except Exception:
            return False
    
    def get_history_summary(self) -> Dict:
        """获取历史记录摘要"""
        history = self.load_history()
        
        if not history:
            return {
                "total_count": 0,
                "date_range": None,
                "latest_analysis": None
            }
        
        # 按时间排序
        history_sorted = sorted(history, key=lambda x: x.get('timestamp', ''))
        
        return {
            "total_count": len(history),
            "date_range": {
                "earliest": history_sorted[0].get('timestamp'),
                "latest": history_sorted[-1].get('timestamp')
            },
            "latest_analysis": history_sorted[-1]
        }
    
    def search_history(self, **filters) -> List[Dict]:
        """
        搜索历史记录
        
        Args:
            **filters: 搜索过滤条件
                - model_name: 商品型号
                - date_from: 开始日期
                - date_to: 结束日期
                - min_profit: 最小利润
                - max_profit: 最大利润
        """
        history = self.load_history()
        filtered_records = []
        
        for record in history:
            if self._match_filters(record, filters):
                filtered_records.append(record)
        
        return filtered_records
    
    def _match_filters(self, record: Dict, filters: Dict) -> bool:
        """检查记录是否匹配过滤条件"""
        # 商品型号过滤
        if 'model_name' in filters:
            model_name = record.get('result', {}).get('商品型号', '')
            if filters['model_name'].lower() not in model_name.lower():
                return False
        
        # 日期范围过滤
        if 'date_from' in filters or 'date_to' in filters:
            timestamp = record.get('timestamp', '')
            if 'date_from' in filters and timestamp < filters['date_from']:
                return False
            if 'date_to' in filters and timestamp > filters['date_to']:
                return False
        
        # 利润范围过滤
        if 'min_profit' in filters or 'max_profit' in filters:
            profit = record.get('result', {}).get('总利润', 0)
            if 'min_profit' in filters and profit < filters['min_profit']:
                return False
            if 'max_profit' in filters and profit > filters['max_profit']:
                return False
        
        return True
    
    def export_history_to_excel(self, filename: str = None) -> str:
        """导出历史记录到Excel"""
        if filename is None:
            filename = f"history_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        history = self.load_history()
        
        if not history:
            raise ValueError("没有历史记录可导出")
        
        # 准备数据
        export_data = []
        for record in history:
            result = record.get('result', {})
            input_data = record.get('input_data', {})
            
            export_row = {
                '分析ID': record.get('analysis_id'),
                '分析时间': record.get('timestamp'),
                '商品型号': result.get('商品型号', ''),
                '商品售价': input_data.get('price', 0),
                '商品成本': input_data.get('cost', 0),
                '销量': result.get('销量', 0),
                '退货数量': result.get('退货数量', 0),
                '成交订单数': result.get('成交订单数', 0),
                '净成交订单数': result.get('净成交订单数', 0),
                '退款率': f"{result.get('退款率', 0):.2f}%",
                '秒退率': f"{result.get('秒退率', 0):.2f}%",
                '总收入': result.get('总收入', 0),
                '总成本': result.get('总成本', 0),
                '总利润': result.get('总利润', 0),
                '利润率': f"{result.get('利润率', 0):.2f}%",
                '广告费用': result.get('广告费用', 0),
                '广告启用': '是' if result.get('广告启用', False) else '否'
            }
            export_data.append(export_row)
        
        # 创建DataFrame并导出
        df = pd.DataFrame(export_data)
        df.to_excel(filename, index=False)
        
        return filename
    
    def get_profit_trend(self) -> Dict:
        """获取利润趋势数据"""
        history = self.load_history()
        
        if len(history) < 2:
            return {"message": "历史记录不足，无法生成趋势"}
        
        # 按时间排序
        history_sorted = sorted(history, key=lambda x: x.get('timestamp', ''))
        
        dates = []
        profits = []
        models = []
        
        for record in history_sorted:
            dates.append(record.get('timestamp', '').split('T')[0])  # 只取日期部分
            profits.append(record.get('result', {}).get('总利润', 0))
            models.append(record.get('result', {}).get('商品型号', ''))
        
        return {
            "dates": dates,
            "profits": profits,
            "models": models,
            "trend_direction": "上升" if profits[-1] > profits[0] else "下降",
            "avg_profit": sum(profits) / len(profits)
        }

# 创建全局历史记录管理器实例
history_manager = HistoryManager()