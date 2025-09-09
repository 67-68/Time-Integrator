


from ti.core.definitions import YESTERDAY, ActionType
from ti.features.detector.matchers import Matcher


""" Complex matchers
这里用来存放config使用的matchers
basically, 和matcher本身在结构中的地位是同构的
被analyzer_config使用来过滤信息
使用matcherall或者matcherany 把不同的matcher结合起来
"""
matcher = Matcher()

YESTERDAY_WORK_MATCHER = matcher.matchAll(
    matcher.date_is(YESTERDAY),
    matcher.action_type_is(ActionType.WORK.value)
)

ANY_MATCHER = matcher.property_is("action")

""" sequence matchers
这里用来存放detector使用的matcher列表
它们和上面的单纯matcher最大的区别就是它们是依次被使用的列表而不是一个单的matcher
它们在结构中的地位：
使用matcher和complex matcher作为它们的元素
它们被detector使用
"""

# 要做一个匹配餐后浪费时间的

"""
在这些配方中(conditional card matchers)
每个列表的item是一个字典
包含着两个key:
状态名称和matcher匹配符
"""
POST_EAT_WASTE = [
    {
        "matcher": matcher.action_is("吃饭"),
        "state_name": "eat"
    },
    {
        "matcher": matcher.action_type_is(ActionType.WASTE.value),
        "state_name":"waste"
    }
]