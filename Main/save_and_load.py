import json

def saveData(actions):
    with open("data.json","w",encoding = "utf-8") as f:
        json.dump(actions,f,ensure_ascii = 4, indent = 4)