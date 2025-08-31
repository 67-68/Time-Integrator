from unittest.mock import MagicMock
from ti.UI.presenters.translator import Translator
from ti.controller.mainCoordinator import MainCoorinator
from ti.dataAccess.insightManager import InsightManager
from ti.engine.insightEngine import InsightEngine

# 我不关心测试内的细节，而是能够履行它在uml图中的义务，接受和传递需要的

class Test_Accept_Conditional_Card:
    # 测试整个卡片功能，包含初始化和生成卡片
    # 包含着三个验收测试，总体的，初始化以及生成卡片的测试
    
    def test_conditional_card_function(
        self,
        mainCoodinator: MainCoorinator,
        mock_analysis_page: MagicMock
        ):
        """
        GIVEN: mainCoodinator, 包含特殊模式的数据源
        WHEN:  mainCoodinator初始化(fixture中已完成)
        THEN:  AnalysisPage的add_cards方法应该被调用，且参数是一个列表
        
        本测试架构来源于[0]generate_report_overview.puml
        """
        # mainCoodinator已经在fixture中初始化，并调用了create_yesterday_report
        
        # 1. 验证 add_cards 方法被调用
        mock_analysis_page.add_cards.assert_called()
        
        # 2. 验证 add_cards 方法只被调用了一次
        mock_analysis_page.add_cards.assert_called_once()
        
        # 3. 获取调用参数
        first_call_args = mock_analysis_page.add_cards.call_args
        
        # 4. 验证调用参数的结构
        # call_args 是一个元组 (args, kwargs)
        # 我们期望只有一个位置参数 (一个列表)，没有关键字参数
        assert len(first_call_args[0]) == 1
        assert len(first_call_args[1]) == 0
        
        # 5. 验证该位置参数是一个列表
        cards_list = first_call_args[0][0]
        assert isinstance(cards_list, list)
        
        # 6. 验证列表不为空 (因为我们的测试数据应该能生成卡片)
        assert len(cards_list) > 0
        
        # 7. (可选) 验证列表中每个元素都是字典
        assert all(isinstance(card, dict) for card in cards_list)