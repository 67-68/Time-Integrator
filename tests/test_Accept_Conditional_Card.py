from unittest.mock import MagicMock
from ti.UI.presenters.translator import Translator
from ti.controller.mainCoodinator import MainCoodinator
from ti.dataAccess.insightManager import InsightManager
from ti.engine.insightEngine import InsightEngine

# 我不关心测试内的细节，而是能够履行它在uml图中的义务，接受和传递需要的

class Test_Accept_Conditional_Card:
    # 测试整个卡片功能，包含初始化和生成卡片
    # 包含着三个验收测试，总体的，初始化以及生成卡片的测试
    
    def test_conditional_card_function(
        self,
        mainCoodinator: MainCoodinator,
        mock_analysis_page: MagicMock  # <-- 请求新的 fixture
        ):
        """
        GIVEN: mainCoodinator, 包含特殊模式的数据源
        WHEN:  mainCoodinator开始初始化
        THEN:  可以看到昨天的Conditional_Card, 并且UI的add_card方法被调用
        
        本测试架构来源于[0]generate_report_overview.puml
        """
        # 已经在mainCoodinator的fixture中初始化并生成了卡片
        
        # 1. 验证 add_card 方法被调用
        mock_analysis_page.add_card.assert_called()
        
        # 2. 打印出第一次调用的参数
        #    call_args[0] 是位置参数 (args)
        #    call_args[1] 是关键字参数 (kwargs)
        first_call_args = mock_analysis_page.add_card.call_args
        print("add_card was called with:", first_call_args)
        
        # 3. 您可以对参数进行更具体的断言
        #    例如，验证第一个参数是一个字典
        assert isinstance(first_call_args[0][0], dict)
        
        # 4. 原有的断言，验证卡片确实生成了
        service = mainCoodinator.service.getServices()
        im: InsightManager = service["IM"]
        cards = im.get_current_cards()
        assert len(cards) > 0