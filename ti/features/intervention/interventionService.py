from dataclasses import dataclass
from ti.UI.presenters.formatter import FormatService
from ti.core.eventBus import EventBus

from ti.domain.detector.baseDetector import BaseDetector
from ti.features.intervention.presenter.cardPresenter import INV_State_Publish, InterventionPresenter
from ti.features.intervention.view.card import InterventionCard
from ti.services.realTimeMonitorService import RealTimeMonitor


class InterventionService():
    """_summary_
    属于Intervention功能
    用来管理和创建现存Intervention
    """
    def __init__(
        self,
        monitor: RealTimeMonitor,
        bus: EventBus
    ):
        self.interventions = {}
        self.monitor = monitor
        self.bus = bus

        events = ["create_intervention"] # 首先使用硬编码，扩展性之后再说吧.或许在配方中加一个key说这个state需要创建

        for event in events:
            self.bus.subscribe(f"{event}_created",self._on_create_intervention)

    def _on_create_intervention(
        self,
        publish_pack:INV_State_Publish # 包含配方和当前的状态, ui
    ): 
        inv_ui = publish_pack.ui # 不用ID, 因为必要的信号传输都包含在ui内。它在创建的时候和presenter连接了。在处理按钮返回的事件之后发出一个关闭模态窗口事件
        detector = publish_pack.recipe.detector # TODO: 这里是类还是实例?
        INV_id = publish_pack.recipe.intervention_id
        
        # 打包
        monitor_pack = INV_Monitor_Pack(inv_ui,detector,INV_id)
        
        # 存档到Monitor
        self.monitor.add_monitor_project({
            "detector": detector,
            "id": INV_id,
            "ui": inv_ui
        })
        print(f"添加项目{INV_id}到监视器")

@dataclass
class INV_Monitor_Pack:
    ui:InterventionCard
    detector:type[BaseDetector]
    INV_id: str