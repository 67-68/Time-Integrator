"""
我暂时的思路就是在其他的py文件里面存universal的function，至于把它们运用起来就放在main，也就是说validation也要在main
首先使用while输入数据,把它转换为通用的json格式
然后validate,如果validate = true 就存进里面
由于是按天数存放的，不可能出现两天一样的情况

额外信息：可能需要在每一步加上debug信息，但那是后面的事情了
"""
import json
from CLI import promptInput

#Main function start
print("welcome to the time-integrater, it is a gadget that helps you to analyze your time distribusion")

promptInput()
        
    
    