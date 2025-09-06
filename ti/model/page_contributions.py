from dataclasses import dataclass


@dataclass
class PageContribution:
    """
    这个数据模型类用来定义
    需要在本体上加载页面的插件
    需要使用的格式
    """
    page_id: str #插件自己的页面id，用来在插件自己的方法中生成页面
    navigation_name: str # 这个页面导航按钮会显示什么
    parent_page: str # 这个页面要放到核心中的哪个页面
    # 可以使用capture/analysis

@dataclass
class PluginPage:
    """
    这个数据模型类用来定义
    插件页面事件发布的时候
    数据的规范
    """