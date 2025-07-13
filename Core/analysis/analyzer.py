"""
首先需要说明,对于所有analyzer
都是输入一个actionUnit, 输出一个dict包裹着的数据
"""


"""
这些函数进行两个actionUnit间的对比
使用方法:在创建好了上面的matcher之后,把matcher输入进来作为条件
"""
def find_sequences(units: list, first_matcher, second_matcher):
    """_summary_
    这个函数输入两个matcher, 首先找出符合firstMatcher的数据，然后找出它下面一条是否符合secondMatcher, 如果符合，把这所有符合的两条au作为dict(key = date)-列表内元组返回
    Args:
        firstMatcher (matcher)
        secondMatcher (matcher)
        data (list)
    """
    sequences = []
    for i in range(len(units) - 1):
        unit1 = units[i]
        unit2 = units[i+1]
        
        # 假设序列必须在同一天内
        if unit1.get("date") != unit2.get("date"):
            continue

        if first_matcher(unit1) and second_matcher(unit2):
            sequences.append([unit1, unit2])
    return sequences
                    
                    
"""
这些函数进行特殊数据的获取，类似极值和平均值
他们接受matcher处理之后的数据
"""
def getTotal_timeSpan(actionUnits):
    total = 0
    for au in actionUnits:
        total += au["timeSpan"]
    return total

def find_longest_timeSpan(actionUnits,config):
    matcher = config["matcher"]
    peak = 0
    data = actionUnits[0]
    for au in actionUnits:
        if matcher(au) and au["timeSpan"] > peak:
            peak = au["timeSpan"]
            data = au
    
    return data