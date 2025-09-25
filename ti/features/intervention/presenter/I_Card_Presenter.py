from abc import abstractmethod
from ti.presenters.BasePresenter import BasePresenter
from ti.services.utils import QtABCMeta


class ICardPresenter(BasePresenter, metaclass=QtABCMeta):
    """
    这个类有两个身份：展示信息和发送事件
    

    Args:
        ABC (_type_): _description
    """
    
    # --- 展示信息的函数 ---
    @abstractmethod
    def apply_presentation(self):
        """
        这个方法用来把实际上获取的Presentation包展示出来
        它接受一个Presentation包
        """
        
    @abstractmethod
    def get_presentation(self):
        """
        这个方法用来获取Presentation
        它接受一个状态，查找Presentation
        """
        
    @abstractmethod
    def get_next_state(self):
        """
        这个方法用来获取下一个状态
        通过当前状态和一个INVViewEvent查找状态
        下一个状态被用来获取Presentation
        """
    
    # --- 用来发送事件的函数 ---
    @abstractmethod
    def _on_button_clicked(self):
        """
        这个函数会接受一个从Button过来的INVViewEvent
        它会通过这个值获取下一个状态
        发送状态附加的事件: Special Events
        以及状态自己转换的事件之后: 
        (ViewState.entering_event)
        切换Presentation
        """
        
    @abstractmethod
    def send_event(self):
        """
        这个函数会接受一个状态，它负责发送这个状态所连带着的所有状态
        首先它会把Speicial_Event打包成为InterventionTriggered事件
        然后通过EventBus的Publish_Event方法发送
        """