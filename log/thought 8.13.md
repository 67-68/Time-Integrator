我发现Cache的存储被调用了两次，虽然理论上来说它应该也使用mock但是先不管这个
两次主要是因为的确有两个卡片，但失败的原因是我给它做了类检测，如果不是list就不能存储
输入进来的东西是dict而非list

下一步是打个断点看看这个到底是什么东西，需不需要特别写一个兼容，
它的报错提示是card[data] unhashable, 我需要看一眼这两个东西是什么

我到了之后发现card是正常卡片，里面有一个data key, 因此大概data忘记加上""了
我加上之后就可以了

仍然报错，发现下面还有一个没有加""的, data和key两个

仍然报错，我发现key不需要加""

仍然报错，我发现上面几行说data变量没有被定义
我打个断点看看什么情况

这里是一个if else的结构，应该是首先看一眼是否这个卡片在数据中，如果不在就初始化相关的数据结构
这个时候应该是第二张卡片进来，和上一张相同，因此结构已经被初始化，也就到了else这里
但是这个data["data"]是什么用意呢？怕不是少了一个self
因此加上 self

然后发现又出问题了，难道是上面初始化了之后没有存入类变量？总之现在需要搞清楚到底想要写什么

仔细看了一下，意图估计是寻找相同id卡片，但是数据结构搞错了，少了一个id
因此加上，变成for c in self.data[id]["data"]:

但我看了一下，self.data[id]["data"]是一个列表，但我要寻找的是card_id, 为什么要从数据里找呢

结构如下
(Pdb) p self.data[id]
{
    'data': 
    [
        {
        'weight': 24, 
        'history': {'post_eat_waste': {...}}, 
        'id': 'post_eat_waste', 
        'data': {
            'meal': {
                'id': '4bba0f00-cad1-4e47-9406-88c55432a667', 
                'date': '2025-08-12', 
                'action': '吃饭', 
                'start': '13:34', 
                'end': '13:51', 
                'action_type': 'rest', 
                'actionDetail': '', 
                'timeSpan': 17, 
                'urgency': False, 
                'importance': False
                }, 
            'waste': {
                'id': 'a5f999e8-2004-4787-a06e-d28c2ab30bfb', 
                'date': '2025-08-12', 
                'action': '小说', 
                'start': '13:51', 
                'end': '13:57', 
                'action_type': 'waste', 
                'actionDetail': '', 
                'timeSpan': 6, 
                'urgency': False, 
                'importance': False
                }
            }, 
        'card_id': 'dc1ad679-62e7-437f-aa12-bfc1930193b6'
        }
    ], 
    'total': {'timeSpan': 24, 'count': 2}
    }


发现又出问题了，line 86
我发现又是一个本地变量的错误，我估计还有更多这样的错误
去吃饭了

我把所有的data都改为了self.allData, 然后还加了[id]
之后我发现后面其实是有把data赋值进allData的

因此我在前面加了一个global variable data

我需要把这个逻辑用uml动态图重新写一遍，有点复杂

失败了，虽然在cards 相加的时候，的确已经有了卡片，但是不知道为什么没有加进去，好像
其实是成功了，加入了真实的UI里面而非我填入的那个Mock UI, 我的测试写错了

{
    'weight': 24, 
    'id': 'post_eat_waste', 
    'data.meal.id': 'df238129-b4d5-47ff-b6b5-992a87b2e238', 
    'data.meal.date': '2025-08-12', 
    'data.meal.action': '吃饭', 
    'data.meal.start': '12:22', 
    'data.meal.end': '12:37', 
    'data.meal.action_type': 'rest', 
    'data.meal.actionDetail': '', 
    'data.meal.timeSpan': 15, 
    'data.meal.urgency': False, 
    'data.meal.importance': False, 
    'data.waste.id': '393aea78-f9e3-4c33-80d0-cfa215795bd6', 
    'data.waste.date': '2025-08-12', 
    'data.waste.action': '短视频', 
    'data.waste.start': '12:37', 
    'data.waste.end': '12:46', 
    'data.waste.action_type': 'waste', 
    'data.waste.actionDetail': '', 
    'data.waste.timeSpan': 9,
    'data.waste.urgency': False,
    'data.waste.importance': False,
    'card_id': '32808e09-e178-482f-b523-19834956ec35'
}