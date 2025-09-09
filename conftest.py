# conftest.py

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from ti.features.detector import userMatchers
from ti.UI.presenters.translator import Translator
from ti.UI.views.MainWindow import MainWindow
from ti.core.mainCoordinator import MainCoorinator
from ti.core.analysis import presenters
from ti.features.detector.baseDetector import BaseDetector
from ti.services.serviceContainer import ServiceContainer
from ti.features.intervention.model.model import INV_Contract, Duration, INV_Contract_State
from ti.features.intervention.service.contractService import INV_ContractService
from ti.features.intervention.service.logger import InterventionLogger

#  ----- 服务 ------
@pytest.fixture
def mock_analysis_page():
    """提供一个带 add_cards 方法的 AnalysisPage (AP) 模拟对象。"""
    mock_ap = MagicMock()
    mock_ap.add_cards = MagicMock()  # 修正: add_card -> add_cards
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
    return MainCoorinator(serviceContainer,UI)

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

# ----- Intervention 测试 fixtures -----

@pytest.fixture
def sample_contract():
    """提供一个用于测试的 Contract 实例"""
    return INV_Contract(
        contract_category_id="post_eat_waste",
        duration=Duration.TODAY.value,
        current_state=INV_Contract_State.AGREED.value,
        view_recipe_id="post_eat_waste",
        detector_recipe_id="post_eat_waste",
        create_time=datetime.now() - timedelta(hours=2)  # 2小时前创建
    )

@pytest.fixture
def expired_contract():
    """提供一个已过期的 Contract 实例"""
    yesterday = datetime.now() - timedelta(days=1, hours=2)  # 昨天创建
    return INV_Contract(
        contract_category_id="post_eat_waste", 
        duration=Duration.TODAY.value,
        current_state=INV_Contract_State.AGREED.value,
        view_recipe_id="post_eat_waste",
        detector_recipe_id="post_eat_waste",
        create_time=yesterday
    )

@pytest.fixture
def mock_contract_repository():
    """提供模拟的 Contract Repository"""
    return MagicMock()

@pytest.fixture
def mock_logger():
    """提供模拟的 InterventionLogger"""
    return MagicMock()

@pytest.fixture
def contract_service(mock_contract_repository, mock_logger):
    """提供配置好的 ContractService 实例"""
    mock_recipe_repos = MagicMock()
    mock_register = MagicMock()
    
    return INV_ContractService(
        contract_repository=mock_contract_repository,
        con_recipe_repos=mock_recipe_repos,
        register=mock_register,
        logger=mock_logger
    )
