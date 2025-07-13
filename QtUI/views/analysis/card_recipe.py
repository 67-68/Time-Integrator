"""
This file store all the recipe of cards
according to their type, stored in different way and access in different way

id: 这个故事的id,因此更容易找到它.(虽然不知道有什么用,但留一个id总不会是坏事)
semantic_type: 这是什么故事？(The 'What')
judgement_type: 这是好是坏？(The 'so what')
card_progress: 故事需要哪些(函数获取的)数据？(The 'With What')
card_appearance: 这个故事的面貌(The 'is what')

对于中间三个key, semantic type, judgement_type和card_appearance, 他们需要被presenter从别的地方获取,填入
对于card_progress, presenter需要按照顺序执行函数并把上一个的产物给下一个
"""

#  ------ card types ------

"""
daily card recipe
These card will all be used in the daily trend function
otherwise, they will not be used at all
"""
DAILY_CARD_RECIPE = [
    {
        "id":"total_time",
        "semantic_type":
        "judgement_type":
        "card_appearance":
        "card_progress":
    }
]


"""
condition card recipe
These card will be used when some weird condition was met
eg. work for 3 hours
"""
#in the future, it can change to a list of cards that each contain the condition as a key, or even maybe a matcher in it and been scanned forth and backwards
CONDITION_CARD_RECIPE = []