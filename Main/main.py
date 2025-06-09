"""
我暂时的思路就是在其他的py文件里面存universal的function，至于把它们运用起来就放在main，也就是说validation也要在main
首先使用while输入数据,把它转换为通用的json格式
然后validate,如果validate = true 就存进里面
由于是按天数存放的，不可能出现两天一样的情况

额外信息：可能需要在每一步加上debug信息，但那是后面的事情了
"""

"""debug 信息
非常务实！以下是你这段代码不修就肯定跑不起来/直接报错/必定逻辑崩溃的地方，其余优化建议一律不说：

⸻

1. 所有未return的函数导致主流程数据为None

比如你的parseDataIntoList、discardSpace等函数没有return，主流程接收的变量会变成None。
表现：一进for循环就报错，或者变量内容是None无法用。

必须修：

def parseDataIntoList(userData):
    # ...
    return actions

def discardSpace(userData):
    # ... 
    return newData  # 或 return userData


⸻

2. 字符串切片/索引用错，直接IndexError或逻辑错

比如在rangeValidation、formatValidation等地方用了：

pre[0:2], pre[2]

如果时间不是固定”hh:mm”格式，pre[2]可能拿到的是”:”，不是数字，一用就报错或逻辑出锅。

必须修：
	•	用split(":")取小时和分钟（不然一定类型或取值错误）

⸻

3. discardSpace实现本身会报错

for i in range(len(1, userData)):

这里的len(1, userData)直接TypeError。
必须修：
	•	应为range(len(userData))

⸻

4. parseDataIntoList没有return会导致actions为None，for循环直接报错

actions = parseDataIntoList(userData)
for i in range(len(actions)):
    # 如果actions为None，TypeError: object of type 'NoneType' has no len()


⸻

只要修好上面这4个地方，代码能跑起来。
	•	每个有“处理数据”的函数最后要return
	•	用split(":")拆时间，不用切片
	•	for循环的range要合法
	•	discardSpace要有输出

⸻

剩下格式健壮性、用户体验等你可以后续慢慢优化，不会影响现在代码是否能“基本能跑”。

需要看更精简修正范本也可以随时要！    
"""
import json
from Main.validations import formatValidation, rangeValidation, timeValidation
from parseInput import discardSpace, parseDataIntoList, timeCompare
from save_and_load import saveData

#Main function start
print("welcome to the time-integrater, it is a gadget that helps you to analyze your time distribusion")

# use a while loop, rather than a function to prompt input
while True:
    #input the data
    userData = input("input your data")
    
    #TODO:presence check
    
    #TODO:use strip to delete spaces
    
    #TODO:change it into discard redundant space in data
    userData = discardSpace(userData)
    
    #change the format of the data, in order to save into json
    userData = userData.split(" - ")
    
    #put data into the list
    actions = parseDataIntoList(userData)
    
    #Format check and change the format
    for i in range (len(actions)):
        actions[i]["end"] = formatValidation(actions[i]["start"],actions[i]["end"])
    
    #validate whether they are reasonable
    if rangeValidation(actions) == True:
        break

#接下来是把数据输入进json
    