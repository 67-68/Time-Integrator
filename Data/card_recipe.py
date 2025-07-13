from Core.analysis import analyzer,matchers,presenters
from Data import userMatchers

"""
This file store all the recipe of cards
according to their type, stored in different way and access in different way

一共有五个在presenter最终处理之前会被添加进一个card unit的key

id: 这个故事的id,因此更容易找到它.(虽然不知道有什么用,但留一个id总不会是坏事)
data: 故事需要哪些(函数获取的)数据？(The 'With What')

sementic_type: 这是什么故事？(The 'What')
judgement_type: 这是好是坏？(The 'so what')
card_appearance: 这个故事的面貌(The 'is what')

对于中间三个key, sementic type, judgement_type和card_appearance, 他们需要被presenter从别的地方获取,填入
对于card_progress, presenter需要按照顺序执行函数并把上一个的产物给下一个

对于实际上会填充的数据,它看起来会是这样:三个key
id:
analyzer: 一个函数和相应的configure设置
presenter: 一个函数

analyzer会首先处理,得出基本的数据和type,会根据configure处理
然后小的presenter(core/analysis/presenter),加入后面三个key
最后大的presenter处理,获取数据，传输给卡片
"""

#  ------ card types ------

"""
daily card recipe
These card will all be used in the daily trend function
otherwise, they will not be used at all
"""
DAILY_CARD_RECIPE = [
    {
        "id":"peak_work_analysis",
        "analyzer": analyzer.find_longest_timeSpan,
        "analyzer_config": {
            "matcher": userMatchers.TODAY_WORK_MATCHER     #matcher我放在了userMatchers文件而不是这里
        },
        "presenter": presenters.present_peak_timeSpan
    }
]


"""
condition card recipe
These card will be used when some weird condition was met
eg. work for 3 hours
"""
#in the future, it can change to a list of cards that each contain the condition as a key, or even maybe a matcher in it and been scanned forth and backwards
CONDITION_CARD_RECIPE = []