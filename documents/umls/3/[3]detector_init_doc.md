# 总览
该文档记录detector初始化的逻辑和各种配置的细节，会根据detector实例的属性展开介绍

首先,detector首先拥有一个基本的类,然后根据传入的config来创建

# 属性
- sequence: list
    用来存储matchers及其顺序

- weight_calc: function
用来存储计算重量的方法，可能从外面导入依赖也可能用内置的
如果config中存在weight_calc键,那么使用传入的这个函数

- _on_weight_calculation(actionUnits: list) -> float
()内置的用来计算重量的方法

- currentIndex: int
当前的状态序号，用来表示当前进行到了第几个状态
最少是0，最多是状态的个数-1

- passed_au: dict
用来存储所有通过检测的au，会在最后作为数据统一发送出去
使用字典，每个au的key name是它的状态名称

- ICS: InsightCacheService
把传入进来的依赖存入自己的变量
会调用它的方法获取数据，作为历史数据
在最后打包的时候传出去
- id: str
获取卡片的id
会在最后打包数据的时候传送出去