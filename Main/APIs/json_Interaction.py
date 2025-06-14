import json    
#这里删除了一个原本的Savedata函数和firstSaveData函数，改用universal saveData函数替代

#在需要覆盖的时候使用
#注意！它不会帮你自动提取之前的东西然后加进去，因此使用函数之前应该手动增加原本的数据，否则可能丢失数据
def saveDataAPI(data,name):
    with open(name,"w",encoding = "utf-8") as f:
        json.dump(data,f,ensure_ascii = False, indent = 4)

    
#这个function会返回name.json的内容，如果为空那么返回一个空的list
def getDataAPI(name):
    try:
        with open(name,"r",encoding = "utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print("there's nothing in the data")
        return {} #把空的返回值修改为了一个字典
