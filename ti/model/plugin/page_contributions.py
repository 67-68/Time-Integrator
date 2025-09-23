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
    create_page_callback: callable = None # 页面创建回调函数
    actual_page = None # 供界面创建之后使用来存储page
    # 可以使用capture/analysis