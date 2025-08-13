# conftest.py

import pytest
from unittest.mock import MagicMock

from Data import userMatchers
from ti.UI.presenters.translator import Translator
from ti.UI.views.MainWindow import MainWindow
from ti.controller.mainCoodinator import MainCoodinator
from ti.core.analysis import presenters
from ti.core.analysis.detectors.detector import BaseDetector 
from ti.services.serviceContainer import ServiceContainer

#  ----- 服务 ------
@pytest.fixture
def mock_analysis_page():
    """提供一个带 add_card 方法的 AnalysisPage (AP) 模拟对象。"""
    mock_ap = MagicMock()
    mock_ap.add_card = MagicMock()
    return mock_ap

@pytest.fixture
def mainWindow(mock_analysis_page):
    """提供一个使用模拟 AP 对象的 MainWindow 模拟对象。"""
    mock_window = MagicMock()
    mock_window.getUIs.return_value = {"AP": mock_analysis_page}
    return mock_window

@pytest.fixture
def UI(mainWindow: MainWindow):
    """_summary_
    返回一个UI Dict
    """
    return mainWindow.getUIs()

@pytest.fixture
def serviceContainer():
    """_summary_

    Returns:
        service: 一个ServiceContainer实例，而不是service列表
    """
    return ServiceContainer()
    

@pytest.fixture
def mainCoodinator(serviceContainer,UI):
    """_summary_
    这个函数作为pytest的fixture,
    返回一个初始化完成的Coodinator
    Args:
        serviceContainer (ServiceContainer): 持有服务

    Returns:
        MainCoodinator: 主管
    """
    return MainCoodinator(serviceContainer,UI)

@pytest.fixture
def post_eat_waste_recipe():
    """这个Fixture只负责提供一个干净的、用于测试的配方。"""
    return [
        {
            "detector": BaseDetector,
            "config": {
                "sequence": userMatchers.POST_EAT_WASTE,
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
def raw_test_data_stream():
    """提供一个原始的数据流，用于测试。"""
    return [
        "14001440r吃饭",
        "14401520s视频"
    ]
