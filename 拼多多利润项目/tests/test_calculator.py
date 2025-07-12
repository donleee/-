#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拼多多利润项目 - 测试文件
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.input_module import ProfitInput
from src.calculation_engine import calculate_profit
from config.settings import Settings

class TestProfitCalculator(unittest.TestCase):
    """利润计算器测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.sample_input = ProfitInput(
            model_name="TEST-SKU001",
            price=100.0,
            cost=50.0,
            other_cost=5.0,
            shipping_fee=10.0,
            commission_rate=0.03,  # 已转换为小数
            sales_volume=100,  # 销量
            return_quantity=10,  # 退货数量
            deal_orders=95,  # 成交订单
            net_deal_orders=85,  # 净成交订单
            post_shipping_refund_ratio=0.0,
            ad_deal_price=2.0,
            ad_enabled=True
        )
    
    def test_basic_profit_calculation(self):
        """测试基本利润计算"""
        result = calculate_profit(self.sample_input, 100)
        
        # 检查返回结果包含所有必要字段
        required_fields = [
            '总利润', '单均利润', '利润率', '总收入', '总成本',
            '成本构成', '保本售价', '保本广告出价', '订单总数',
            '销量', '退货数量', '成交订单数', '净成交订单数', 
            '退款率', '秒退率', '广告费用', '广告启用'
        ]
        
        for field in required_fields:
            self.assertIn(field, result)
        
        # 检查数值合理性
        self.assertGreater(result['总收入'], 0)
        self.assertGreater(result['总成本'], 0)
        self.assertEqual(result['订单总数'], 100)
        self.assertGreater(result['净成交订单数'], 0)
        self.assertEqual(result['广告启用'], True)
        self.assertGreater(result['广告费用'], 0)
        self.assertEqual(result['销量'], 100)
        self.assertEqual(result['退货数量'], 10)
        self.assertEqual(result['成交订单数'], 95)
        self.assertEqual(result['净成交订单数'], 85)
    
    def test_no_ads_scenario(self):
        """测试无广告场景"""
        no_ad_input = ProfitInput(
            model_name="TEST-SKU002",
            price=100.0,
            cost=50.0,
            other_cost=5.0,
            shipping_fee=10.0,
            commission_rate=0.03,
            sales_volume=100,
            return_quantity=10,
            deal_orders=95,
            net_deal_orders=85,
            post_shipping_refund_ratio=0.0,
            ad_deal_price=0.0,
            ad_enabled=False
        )
        
        result = calculate_profit(no_ad_input, 100)
        
        self.assertEqual(result['广告启用'], False)
        self.assertEqual(result['广告费用'], 0)
        self.assertNotIn('广告费用', result['成本构成'])
    
    def test_ad_cost_calculation(self):
        """测试广告费用计算"""
        result = calculate_profit(self.sample_input, 100)
        
        # 广告费用 = 分析订单数 × 每笔广告出价
        # 分析订单数 = 100，广告出价 = 2元
        expected_ad_cost = 100 * 2.0
        self.assertAlmostEqual(result['广告费用'], expected_ad_cost, places=2)
        
        # 成本构成应该包含广告费用
        self.assertIn('广告费用', result['成本构成'])
        self.assertEqual(result['成本构成']['广告费用'], expected_ad_cost)
    
    def test_break_even_ad_cost(self):
        """测试保本广告费用计算"""
        result = calculate_profit(self.sample_input, 100)
        
        # 保本广告费用应该存在且大于0
        self.assertIsNotNone(result['保本广告出价'])
        self.assertGreater(result['保本广告出价'], 0)
        
        # 保本广告费用应该是合理的（不考虑退货率）
        max_ad_cost = self.sample_input.price * (1 - self.sample_input.commission_rate) - \
                     self.sample_input.cost - self.sample_input.other_cost - self.sample_input.shipping_fee
        self.assertAlmostEqual(result['保本广告出价'], max_ad_cost, places=2)
        
        # 应该有最高广告投入字段
        self.assertIn('最高广告投入', result)
    
    def test_high_ad_cost_scenario(self):
        """测试高广告费用场景"""
        # 使用很低的售价来创建高广告费用场景
        high_ad_input = ProfitInput(
            model_name="TEST-SKU003",
            price=70.0,  # 低售价，保本广告费用为负或很低
            cost=50.0,
            other_cost=5.0,
            shipping_fee=10.0,
            commission_rate=0.03,
            sales_volume=100,
            return_quantity=10,
            deal_orders=95,
            net_deal_orders=85,
            post_shipping_refund_ratio=0.0,
            ad_deal_price=40.0,  # 这个参数现在不影响计算
            ad_enabled=True
        )
        
        result = calculate_profit(high_ad_input, 100)
        
        # 保本广告费用 = 70 × (1-0.03) - 50 - 5 - 10 = 2.9元
        # 广告费用 = 100 × 2.9 × (1-0.10) = 261元
        # 利润可能为负数，但不一定
        self.assertIsNotNone(result['总利润'])
        self.assertGreater(result['广告费用'], 0)
    
    def test_zero_profit_scenario(self):
        """测试零利润场景"""
        # 使用基于分析订单数的计算逻辑
        # 收入 = 100 × 100 = 10000元
        # 平台扣点 = 10000 × 0.03 = 300元
        # 商品成本 = 100 × (50+5+10) = 6500元
        # 广告费用 = 100 × ad_price
        # 要让总利润为0：10000 - 300 - 6500 - 广告费用 = 0
        # 广告费用 = 3200，所以 ad_price = 3200 / 100 = 32
        
        zero_profit_input = ProfitInput(
            model_name="TEST-SKU004",
            price=100.0,
            cost=50.0,
            other_cost=5.0,
            shipping_fee=10.0,
            commission_rate=0.03,
            sales_volume=100,
            return_quantity=10,  # 10% 退货率
            deal_orders=95,
            net_deal_orders=85,
            post_shipping_refund_ratio=0.0,
            ad_deal_price=32.0,  # 调整广告出价使利润为0
            ad_enabled=True
        )
        
        result = calculate_profit(zero_profit_input, 100)
        self.assertAlmostEqual(result['总利润'], 0, places=0)
    
    def test_break_even_price_with_ads(self):
        """测试包含广告的保本售价"""
        result = calculate_profit(self.sample_input, 100)
        
        # 保本售价 = (商品成本 + 其他成本 + 运费 + 广告出价) / (1 - 平台扣点率)
        # 单位成本 = 50 + 5 + 10 + 2.0 = 67元
        expected_break_even = 67.0 / (1 - 0.03)
        self.assertAlmostEqual(result['保本售价'], expected_break_even, places=2)
    
    def test_cost_breakdown_with_ads(self):
        """测试包含广告的成本构成"""
        result = calculate_profit(self.sample_input, 100)
        
        cost_breakdown = result['成本构成']
        self.assertIn('商品成本', cost_breakdown)
        self.assertIn('运费', cost_breakdown)
        self.assertIn('平台扣点', cost_breakdown)
        self.assertIn('广告费用', cost_breakdown)
        
        # 检查成本构成总和
        total_cost_from_breakdown = sum(cost_breakdown.values())
        self.assertAlmostEqual(total_cost_from_breakdown, result['总成本'], places=2)

class TestSettings(unittest.TestCase):
    """配置测试类"""
    
    def test_settings_validation(self):
        """测试配置验证"""
        # 测试有效数据
        valid_data = {
            'price': 100.0,
            'cost': 50.0,
            'commission_rate': 0.03,
            'refund_rate': 0.10
        }
        
        errors = Settings.validate_input(valid_data)
        self.assertEqual(len(errors), 0)
        
        # 测试无效数据
        invalid_data = {
            'price': -10.0,  # 负价格
            'cost': 50.0,
            'commission_rate': 0.25,  # 超过最大佣金率
            'refund_rate': 0.60  # 超过最大退款率
        }
        
        errors = Settings.validate_input(invalid_data)
        self.assertGreater(len(errors), 0)
        self.assertIn('price', errors)
        self.assertIn('commission_rate', errors)
        self.assertIn('refund_rate', errors)

class TestIntegration(unittest.TestCase):
    """集成测试类"""
    
    def test_complete_workflow_with_ads(self):
        """测试包含广告的完整工作流程"""
        # 创建输入数据
        input_data = ProfitInput(
            model_name="TEST-SKU005",
            price=120.0,
            cost=60.0,
            other_cost=8.0,
            shipping_fee=12.0,
            commission_rate=0.04,
            sales_volume=200,
            return_quantity=20,
            deal_orders=190,
            net_deal_orders=170,
            post_shipping_refund_ratio=0.0,
            ad_deal_price=3.0,
            ad_enabled=True
        )
        
        # 计算利润
        result = calculate_profit(input_data, 200)
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertIn('总利润', result)
        self.assertIn('利润率', result)
        self.assertIn('广告费用', result)
        self.assertTrue(result['广告启用'])
        
        # 验证数值逻辑
        self.assertEqual(result['订单总数'], 200)
        self.assertLessEqual(result['净成交订单数'], 200)
        self.assertGreaterEqual(result['净成交订单数'], 0)
        self.assertGreater(result['广告费用'], 0)
    
    def test_complete_workflow_without_ads(self):
        """测试不包含广告的完整工作流程"""
        # 创建输入数据
        input_data = ProfitInput(
            model_name="TEST-SKU006",
            price=120.0,
            cost=60.0,
            other_cost=8.0,
            shipping_fee=12.0,
            commission_rate=0.04,
            sales_volume=200,
            return_quantity=20,
            deal_orders=190,
            net_deal_orders=170,
            post_shipping_refund_ratio=0.0,
            ad_deal_price=0.0,
            ad_enabled=False
        )
        
        # 计算利润
        result = calculate_profit(input_data, 200)
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertIn('总利润', result)
        self.assertIn('利润率', result)
        self.assertFalse(result['广告启用'])
        self.assertEqual(result['广告费用'], 0)
        self.assertNotIn('广告费用', result['成本构成'])

if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)