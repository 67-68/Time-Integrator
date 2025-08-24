from ti.UI.presenters.formatter import FormatService
from ti.UI.presenters.interventionPresenter import InterventionPresenter
from ti.services.realTimeMonitorService import RealTimeMonitor


class InterventionService():
    """_summary_
    属于Intervention功能
    用来管理和创建现存Intervention
    """
    def __init__(
        self,
        monitor: RealTimeMonitor,
        FS : FormatService
    ):
        self.interventions = {}
        self.monitor = monitor
        self.FS = FS

    def create_intervention(
        self,
        intervention_init_pack #按理来说包含ui,id和detector 2 keys
    ): 
        inter_id = intervention_init_pack["id"]
        inter_ui = intervention_init_pack["ui"]
        detector = intervention_init_pack["detector"]
        state = intervention_init_pack["state"]
        
        self.interventions[inter_id] = InterventionPresenter(inter_ui,state,self.FS)
        
        # 打包
        monitor_pack = {
            "id":inter_id,
            "ui":inter_ui,
            "detector":detector
        }
        
        # 存档到Monitor
        self.monitor.add_monitor_project(monitor_pack)