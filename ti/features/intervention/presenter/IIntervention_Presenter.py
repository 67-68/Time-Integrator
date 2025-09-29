

from abc import abstractmethod
from ti.features.intervention.model.stored.inv_real_time_annoying import RealTimeAnnoying
from ti.presenters.BasePresenter import BasePresenter
from ti.services.utils import QtABCMeta


class IInterventionPresenter(BasePresenter, metaclass=QtABCMeta):
    
    # --- RealTimeAnnoying功能 -- 
    @abstractmethod
    def register_intervention(self,data: RealTimeAnnoying):
        """
        登记Intervention
        目前仅支持登记一个
        如果发现已经有一个在类变量那么print
        """
        pass
    
    @abstractmethod
    def is_pass_due(self):
        """
        根据开始时间和当前时间检验是否需要开始响铃
        如果需要，输出True
        """
        pass
    
    @abstractmethod
    def intervene_user(self):
        """
        调用Mac的通知
        跳出弹窗干扰用户
        显示Detail以及让她回到界面点击停止
        """
        pass
    
    @abstractmethod
    def run_life_cycle(self):
        """
        检验所有Intervention
        调用is_pass_due
        如果True，调用
        """
        pass
    
    