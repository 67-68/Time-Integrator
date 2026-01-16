from enum import Enum

class PluginEvents(Enum):
    PLUGIN_CREATED = "plugin_created" # 用来表示一个插件的加载
    PAGE_PLUGIN_CREATED = "page_plugin_created" # 表示一个有着page的plugin被创建了