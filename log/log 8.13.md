这是8/23的编程记录，具体思路参见 log/thought 8.23.md

## 改动
1. 能否进行进一步的拆分，把固定的每日卡片信息从ReportPresenter中拆分？已经拆分完成，由cardController调用
2. 由cardController给Generators提供配方，数据和服务，按需提供
3. 从app类到controller一路传送一个数据包，各级按需取用
4. 在app类创建了数据包并打算一路传递到contorller
5. 在创建mainCoodinator的时候把数据作为依赖传递了
6. 写了初始化, 从coodinator到generator
7. 写了cardController的生成报告，调用了两个generator类
8. 清除了analysis page的多余卡片生成代码
9. 往analysis page中增加了卡片填充代码
10. 写了新的UI和contrll绑定
    - app类增加了init方法调用
    - coodinator增加了controller获取
    - mainwindow增加了ui获取
    - cardController增加了ui绑定
11. engine和manager新的交互
    - 修改engine卡片检测到之后直接添加数据到manager为发送元组信号
    - Conditional_ReportGenerator检测信号并转接到manager, 使用一个函数
12. 新的controller和UI绑定机制
    - 原本的绑定在创建之后，但创建的时候就需要把卡片塞进UI, 因此把UI作为依赖
13. 修改了insightCache的添加历史记录函数，让其真正可以调用
14. 把controller的ui填充放入依赖,并建构了依赖链条


## 疑惑
2. 对于卡片状态的持有，是使用列表还是字典？controller持有？
3. 对于卡片状态的持有如果是字典，根据卡片id来作为标识？
4. 或许需要给controller写一个基类，然后方便绑定ui什么的？
5. 我需要找一种方法来表示为什么app类初始化的顺序不能乱改


## 解决的疑惑
1. 
    - 如果需要使用controller来管理GUI，那么它就需要持有GUI的实例，但GUI是被提升上去的，没有办法这么搞，难道要使用信号和槽？但是也不行...如果需要使用信号，那么GUI需要持有controller的实例，但它被中央coodinator创建
    得个办法把UI的实例塞进controller, 在创建之后而不是init方法，ui的实例由mainwindow 管理。难道需要app来做这件事情？倒也不是不行，就是需要写一个方法从main window获取所有的实例
    - 就这么搞了，使用app类管理

2. 
    - Engine如何和manager交互呢？它需要持有一个manager实例，然后调用函数往里面放东西吗？
    也就是说，你希望借由第三方，一个同时持有engine和manager实例的第三方，完成他们的通讯？那么为什么不选择生成卡片报告这个功能的宗主 - reportgenerator呢？亦或者serviceContainer? 亦或者这么一点的耦合同样也是可以接受的？
    - 选择在Conditional_ReportGenerator中交互

3. 
    - 发现app类本来就有一个刷新的方法，在想是否要借它的路子来传递依赖，正好也刷新了，但还是先走coodinator
    - 斩断了这个方法，没用了，写了pass

## 代办
1. cache无法保存卡片数据
2. 历史数据的sementic_key, 这个没有测试
3. 需要整一个sementic_key对应的文档，在写narrative的时候方便

## 暂存上下文
我写到修改ReportPresenter
往上是初始化cardController
使用了uml辅助

大概写好了初始化，但是在把数据从controller传入analysis Page展示这一步卡住了
在实际运行的时候发现engine的初始化有问题，传入的并不是一个服务包



