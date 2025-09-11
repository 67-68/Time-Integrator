from dataclasses import dataclass
from enum import Enum

from ti.model.page_contributions import PageContribution

class Events(Enum):
    PLUGIN_EVENTS = "PluginEvents"
        

@dataclass
class PluginPage:
    """
    这个数据模型类用来定义
    插件页面事件发布的时候
    数据的规范
    """
    page_contribution: PageContribution
    ui = None #这里或许需要定义一个插件页面统一的接口
    
class PluginEvents(Enum):
    PLUGIN_CREATED = "plugin_created" # 用来表示一个插件的加载
    PAGE_PLUGIN_CREATED = "page_plugin_created" # 表示一个有着page的plugin被创建了