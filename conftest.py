# conftest.py

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from ti.features.detector.model import userMatchers
from ti.core.mainCoordinator import MainCoorinator
from ti.features.detector.model.baseDetector import BaseDetector
from ti.services.serviceContainer import ServiceContainer


#  ----- 服务 ------
@pytest.fixture
def mock_analysis_page():
    """提供一个带 add_cards 方法的 AnalysisPage (AP) 模拟对象。"""
    mock_ap = MagicMock()
    mock_ap.add_cards = MagicMock()  # 修正: add_card -> add_cards
    return mock_ap

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
    return MainCoorinator(serviceContainer,UI)

