class TestInsightEngine:
    # tests/test_engine.py

    # 我们在这里，严格遵守“准备-执行-断言”的神圣三位一体 (Arrange-Act-Assert)

    def test_engine_correctly_detects_sequence_pattern(
        self,
        configured_insight_engine, # <-- 道具1: 已配置好的引擎
        translator,              # <-- 道具2: 翻译器
        raw_test_data_stream     # <-- 道具3: 原始数据
    ):
        """
        GIVEN: 一个配置为检测“餐后浪费”的引擎，和一个包含该模式的数据流。
        WHEN:  我们将数据流逐一处理并喂给引擎。
        THEN:  引擎应该能成功生成一个符合预期的洞察卡片。
        """
        newData = []
        
        for au in raw_test_data_stream:
            newData.append(translator.fastToProper(au)["data"])
        
        for d in newData:
            configured_insight_engine(d)
        
        cards = configured_insight_engine.get_cur_cards()
        
        
        assert len(cards) == 1
        assert cards[0]["id"] == "post_eat_waste"
        