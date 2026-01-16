from PyQt6.QtCore import pyqtSignal,QObject

from ti.features.detector.model.model import BaseDetectorState, Detector_Config

class BaseDetector(QObject):
    """
    它曾经被设计为所有detector的父类
    但写得太好导致自己+config可以干所有活
    因此直接使用它了
    它负责管理所有detector共用的方法 例如call和状态管理
    
    它的使用方法为: 输入config 和insight service cache, 创建一个实例
    
    然后直接类似普通函数一样调用
    """
    hook_pattern_detected = pyqtSignal(dict)
    pattern_detected = pyqtSignal(dict)
    
    def __init__(
        self,
        config: Detector_Config
    ):
        """
        输入一个config来创建 

        一般包含: 
        分别包含matcher和state name的sequence key
        , 一个权重计算器（也可以不写), 一个id
        """
        super().__init__()
        
        # 存储config
        self.config = config
        
        # 获取matchers
        self.sequence = config.sequence
        self.hooks = self.sequence.hook
        self.results = self.sequence.result
            
        # 获取权重计算函数 如果没有那么使用默认的
        self.weight_calc = self._on_weight_calculation
        
        # ------ 创建状态 ------
            
        # 目前状态
        self.currentIndex = 0
        self.currentState = BaseDetectorState.HOOK.value
        
        # 通过的au
        self.passed_au = {} #使用字典 也可以表示不同阶段
        
        # 历史管理 - 现在通过YamlRepository管理，不再需要单独的缓存服务
        
        # 卡片id
        self.id = config.card_type_id
    
    def process_action_unit(self,au):
        """_summary_
        这个函数用来验证是否输入进来的actionUnit符合当前阶段要求
        如果不符合 返回False, 反之直接进入下一个阶段
        Args:
            au (ActionUnit): 一个行动单元
        """
        if self.currentState == BaseDetectorState.HOOK.value:
            current_state_matcher = self.hooks
        else:
            current_state_matcher = self.results
        
        currentMatcher = current_state_matcher[self.currentIndex].matcher
        
        if currentMatcher(au) == True:    
            """
            这个函数用来进入下一个阶段 它的职责包括：
            修改currentIndex
            判断是否满足了所有条件 如果满足了 自动调用完成函数
            """
            state_name = current_state_matcher[self.currentIndex].state_name
            self.passed_au[state_name] = au
            
            self.currentIndex += 1
            
            if self.currentState == BaseDetectorState.HOOK.value:
                if self.currentIndex >= len(self.hooks):
                    self.currentState = BaseDetectorState.RESULT.value
                    self.currentIndex = 0
                    self.hook_pattern_detected.emit(self.packer())
                    
            elif self.currentState == BaseDetectorState.RESULT.value:
                if self.currentIndex >= len(self.results):
                    self._on_state_complete()
        else:
            if self.currentIndex > 0:
                self.reset()
            
        
    
    def _on_state_complete(self):
        """
        这个函数会在所有状态完成的时候被调用
        它的职责包括:
        - 重新开始状态计数
        - 调用packer函数打包
            - 调用权重计算器计算权重
        - 发出信号
        """
        self.reset()
        self.pattern_detected.emit(self.packer())
        
    def reset(self):
        self.currentIndex = 0
        self.currentState = BaseDetectorState.HOOK.value

    def packer(self) -> dict:
        """
        用来打包
        它会打包: 重要程度,所有匹配的行动单元,卡片类型id
        """
        data = {
            "weight": self.weight_calc(self.passed_au),
            "data": self.passed_au,
            "id": self.id
        }
        
        return data
        
    
    def _on_weight_calculation(self,actionUnits: list) -> float:
        """_summary_
        这个函数是默认的权重计算器
        它会take in所有用到的actionUnit 获取它们的时间信息
        然后根据时间多少算出权重
        Returns:
            float: _description_
        """
        total = 0
        for state_name in actionUnits:
            total += actionUnits[state_name].timeSpan
        return total