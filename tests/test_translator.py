"""
这个测试为了验证翻译器的正确性
"""


from ti.UI.presenters.translator import Translator

class TestTranslator:
    def test_translator(
        self,
        translator: Translator,
        raw_test_data_stream
    ):
        """
        GIVEN: 一个速记语法的翻译器 一个使用正确语法的数据流
        WHEN: 将数据流输入速记语法的翻译器
        THEN: 翻译器可以成功解析速记语法
        """

        translated_data = []
        for au in raw_test_data_stream:
            translated_data.append(translator.fastToProper(au))
        
        data = translated_data[0]["data"]
        
        assert data["start"] == "14:00"
        assert data["end"] == "14:40"
        assert data["action_type"] == "rest"
        assert data["action"] == "吃饭"