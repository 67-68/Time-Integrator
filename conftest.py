# conftest.py

import pytest

from Data import userMatchers
from ti.UI.presenters.translator import Translator
from ti.core.analysis import presenters
from ti.core.analysis.detectors.detector import BaseDetector # 假设这是你的SequenceDetector
from ti.engine.insightEngine import InsightEngine

@pytest.fixture
def post_eat_waste_recipe():
    """这个Fixture只负责提供一个干净的、用于测试的配方。"""
    return [
        {
            "detector": BaseDetector,
            "config": {
                "matchers": userMatchers.POST_EAT_WASTE,
                "id": "post_eat_waste"
            },
            "presenter": presenters.present_sequence_data
        }
    ]

@pytest.fixture
def translator():
    """提供一个Translator实例。"""
    return Translator()

@pytest.fixture
def configured_insight_engine(post_eat_waste_recipe):
    """
    提供一个已经根据特定配方，配置好的InsightEngine实例。
    注意：它依赖于上面的'post_eat_waste_recipe' fixture！
    """
    return InsightEngine(post_eat_waste_recipe)

@pytest.fixture
def raw_test_data_stream():
    """提供一个原始的数据流，用于测试。"""
    return [
        "14001440r吃饭",
        "14401520s视频"
    ]