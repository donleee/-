"""
拼多多利润项目配置文件
"""

import os
from typing import Dict, Any

class Settings:
    """项目配置类"""
    
    # 应用配置
    APP_NAME = "拼多多利润分析系统"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///profit_analysis.db")
    
    # 文件路径配置
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    
    # 确保目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # 默认计算参数
    DEFAULT_ORDER_COUNT = 100
    DEFAULT_COMMISSION_RATE = 0.03  # 3%
    DEFAULT_REFUND_RATE = 0.10      # 10%
    DEFAULT_INSTANT_REFUND_RATE = 0.05  # 5%
    DEFAULT_AD_DEAL_PRICE = 0.0  # 默认无广告费用
    DEFAULT_AD_ENABLED = False       # 默认不启用广告
    
    # 拼多多平台配置
    PINDUODUO_CONFIG = {
        "platform_name": "拼多多",
        "default_commission_rates": {
            "general": 0.03,        # 一般类目3%
            "digital": 0.05,        # 数码类目5%
            "clothing": 0.04,       # 服装类目4%
            "home": 0.035,          # 家居类目3.5%
            "beauty": 0.06,         # 美妆类目6%
        },
        "shipping_fee_ranges": {
            "light": (5, 12),       # 轻货物运费范围
            "heavy": (15, 25),      # 重货物运费范围
            "special": (20, 50),    # 特殊商品运费范围
        },
        "ad_cost_ranges": {
            "low": (0.5, 2.0),      # 低广告费用范围
            "medium": (2.0, 5.0),   # 中等广告费用范围
            "high": (5.0, 15.0),    # 高广告费用范围
        }
    }
    
    # 报告配置
    REPORT_CONFIG = {
        "export_formats": ["xlsx", "csv", "pdf"],
        "chart_colors": {
            "profit": "#2E8B57",
            "cost": "#DC143C",
            "revenue": "#4169E1",
            "ad_cost": "#FF6347",
            "background": "#F8F8FF"
        },
        "decimal_places": 2,
    }
    
    # 风险控制配置
    RISK_CONFIG = {
        "max_refund_rate": 0.5,     # 最大退款率50%
        "max_commission_rate": 0.2,  # 最大佣金率20%
        "min_profit_margin": 0.05,   # 最小利润率5%
        "max_ad_cost_ratio": 0.3,    # 最大广告费用占比30%
        "warning_thresholds": {
            "low_profit": 0.1,       # 低利润警告阈值10%
            "high_refund": 0.2,      # 高退款率警告阈值20%
            "high_cost": 0.8,        # 高成本占比警告阈值80%
            "high_ad_cost": 0.2,     # 高广告费用占比警告阈值20%
        }
    }
    
    # 日志配置
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.FileHandler",
                "filename": os.path.join(LOGS_DIR, "app.log"),
                "mode": "a",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "file"],
                "level": "DEBUG",
                "propagate": False
            }
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """获取所有配置"""
        return {
            "app": {
                "name": cls.APP_NAME,
                "version": cls.VERSION,
                "debug": cls.DEBUG,
            },
            "database": {
                "url": cls.DATABASE_URL,
            },
            "paths": {
                "base_dir": cls.BASE_DIR,
                "data_dir": cls.DATA_DIR,
                "output_dir": cls.OUTPUT_DIR,
                "logs_dir": cls.LOGS_DIR,
            },
            "defaults": {
                "order_count": cls.DEFAULT_ORDER_COUNT,
                "commission_rate": cls.DEFAULT_COMMISSION_RATE,
                "refund_rate": cls.DEFAULT_REFUND_RATE,
                "instant_refund_rate": cls.DEFAULT_INSTANT_REFUND_RATE,
                "ad_deal_price": cls.DEFAULT_AD_DEAL_PRICE,
                "ad_enabled": cls.DEFAULT_AD_ENABLED,
            },
            "pinduoduo": cls.PINDUODUO_CONFIG,
            "report": cls.REPORT_CONFIG,
            "risk": cls.RISK_CONFIG,
            "logging": cls.LOGGING_CONFIG,
        }
    
    @classmethod
    def validate_input(cls, data: Dict[str, Any]) -> Dict[str, str]:
        """验证输入数据"""
        errors = {}
        
        # 检查必要字段
        required_fields = ['price', 'cost', 'commission_rate', 'refund_rate']
        for field in required_fields:
            if field not in data or data[field] is None:
                errors[field] = f"{field} 是必需的"
        
        # 检查数值范围
        if 'price' in data and data['price'] <= 0:
            errors['price'] = "商品价格必须大于0"
        
        if 'cost' in data and data['cost'] < 0:
            errors['cost'] = "商品成本不能为负数"
        
        if 'commission_rate' in data:
            if data['commission_rate'] < 0 or data['commission_rate'] > cls.RISK_CONFIG['max_commission_rate']:
                errors['commission_rate'] = f"佣金率必须在0到{cls.RISK_CONFIG['max_commission_rate']*100}%之间"
        
        if 'refund_rate' in data:
            if data['refund_rate'] < 0 or data['refund_rate'] > cls.RISK_CONFIG['max_refund_rate']:
                errors['refund_rate'] = f"退款率必须在0到{cls.RISK_CONFIG['max_refund_rate']*100}%之间"
        
        # 检查广告费用
        if 'ad_deal_price' in data and data['ad_deal_price'] < 0:
            errors['ad_deal_price'] = "广告费用不能为负数"
        
        # 检查广告费用占比
        if 'price' in data and 'ad_deal_price' in data and data['price'] > 0:
            ad_cost_ratio = data['ad_deal_price'] / data['price']
            if ad_cost_ratio > cls.RISK_CONFIG['max_ad_cost_ratio']:
                errors['ad_deal_price'] = f"广告费用占比不能超过{cls.RISK_CONFIG['max_ad_cost_ratio']*100}%"
        
        return errors
    
    @classmethod
    def get_ad_cost_suggestion(cls, price: float, category: str = "general") -> Dict[str, float]:
        """获取广告费用建议"""
        commission_rate = cls.PINDUODUO_CONFIG["default_commission_rates"].get(category, 0.03)
        
        # 建议广告费用不超过单品利润的20%
        max_suggested_ad_cost = price * (1 - commission_rate) * 0.2
        
        return {
            "conservative": max_suggested_ad_cost * 0.3,  # 保守建议
            "moderate": max_suggested_ad_cost * 0.6,      # 适中建议
            "aggressive": max_suggested_ad_cost * 0.9,    # 激进建议
        }

# 创建全局配置实例
settings = Settings()