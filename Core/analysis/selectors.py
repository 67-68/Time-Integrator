"""
这些函数进行数据的处理
把收集完成的actionUnit进行拆分
例如sequence matcher 处理后的两层[]
输出一个大的actionUnit列表
一个matcher对应一个parser
"""
def sequenceDataParser(data,position):
    """_summary_
    data:其他matcher处理之后的数据
    position: first/second/all, 决定获取哪些数据
    """
    list = []
    newList = []
    if position == "first":
        i = 0
    elif position == "second":
        i = 1
    elif position == "all":
        i = 0
        newList = sequenceDataParser(data,"second") #使用一个递归来处理两种都需要的情况
    
    for auList in data:
        list.append(auList[i])
        
    return list.append(newList)