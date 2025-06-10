import json

def firstSaveData(actions):
    with open("data.json","w",encoding = "utf-8") as f:
        json.dump(actions,f,ensure_ascii = False, indent = 4)
    
def saveData(date,actions):
    data = getData()
    data[date] = actions
    with open("data.json","w",encoding = "utf-8") as f:
        json.dump(data,f,ensure_ascii = False, indent = 4)

#这个function会返回data.json的内容，如果为空那么返回一个空的list
#不需要传入parameter
def getData():
    try:
        with open("data.json","r",encoding = "utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print("there's nothing in the data")
        return []