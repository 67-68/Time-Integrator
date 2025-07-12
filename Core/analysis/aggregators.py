"""
这些函数进行特殊数据的获取，类似极值和平均值
他们接受matcher处理之后的数据
"""
def getTotal_TimeSpan(actionUnits):
    total = 0
    for au in actionUnits:
        total += au["timeSpan"]
    return total