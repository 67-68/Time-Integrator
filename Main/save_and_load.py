import json

def firstSaveData(actions):
    with open("data.json","w",encoding = "utf-8") as f:
        json.dump(actions,f,ensure_ascii = False, indent = 4)
    
def saveData(date,actions):
    data = getData()
    data[date] = actions
    with open("data.json","w",encoding = "utf-8") as f:
        json.dump(data,f,ensure_ascii = False, indent = 4)

def getData():
    with open("data.json","r",encoding = "utf-8") as f:
        data = json.load(f)
        return data