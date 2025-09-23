import json
import yaml
from ti.services.utils import resource_path


#在需要覆盖的时候使用
#注意！它不会帮你自动提取之前的东西然后加进去，因此使用函数之前应该手动增加原本的数据，否则可能丢失数据
def saveData(data,name):
    name = resource_path(name)
    
    with open(name,"w",encoding = "utf-8") as f:
        json.dump(data,f,ensure_ascii = False, indent = 4)

    
#这个function会返回name.json的内容，如果为空那么返回一个空的list
def getData(name):
    name = resource_path(name)
    try:
        with open(name,"r",encoding = "utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print("there's nothing in the data")
        return {} #把空的返回值修改为了一个字典

#UNIVERSAL; INPUT dataLoc and keys; UPDATE all actionUnit with key provided
def updateDataKey(dataLoc,keyToUpdate):
    data = getData(dataLoc)
    for date in data:
        for actionUnits in data[date]:
            for key in keyToUpdate:
                if key not in actionUnits:
                    actionUnits[key] = None

    saveData(data,dataLoc)


def get_yaml_data(file_path):
    """
    读取YAML文件数据
    
    Args:
        file_path: YAML文件路径
        
    Returns:
        dict: YAML文件内容，如果文件不存在或读取失败返回空字典
    """
    file_path = resource_path(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if data is not None else {}
    except FileNotFoundError:
        print(f"YAML file not found: {file_path}")
        return {}
    except Exception as e:
        print(f"Error reading YAML file {file_path}: {e}")
        return {}


def save_yaml_data(data, file_path):
    """
    保存数据到YAML文件
    
    Args:
        data: 要保存的数据
        file_path: YAML文件路径
    """
    file_path = resource_path(file_path)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    except Exception as e:
        print(f"Error saving YAML file {file_path}: {e}")


    


