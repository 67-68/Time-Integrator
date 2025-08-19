## 记录
- 完成了对于大图控制流的修改
- 修改了三张小图
- 发现了新的uml绘图模式
- 把新的Intervention配方使用数据模型类，当前的配方暂时不改
- 修改了ServiceContainer， 添加了新的服务
- 把ServiceContainer类变为了数据模型类
- 增加了intervention_recipe文件
- 在card_recipe中增加了intervention key
- 在InsightEngine打包中增加了intervention
- 在CardController rawdata中增加了intervention
- 在Presenter中增加了处理intervention的部分
- 在narrativ中增加了Intervention_text
- 在formatter中增加了intervention打包
- 在trendCard UI中新增了Intervention的Widget
- 新增了Intervention Card类
- 在AnalysisPage的创建trendCard中加入了创建InterventionCard的配方

## 代办
- 需要搞新的Documents/umls/1/[1]InterventionCard_init.puml序列图
- 需要写Intervention_User_Creation.md的设计文档
    - 同时，把它放进层级图内
- 需要添加新的数据模型到Documents/DATA_DICTIONARY.md
- 在temp.puml中修改之前的大图，因为发现控制流有问题，停滞在group1 -> group2的部分，不知道如何合理的让控制流保持在controller上
- 让gemini CLI帮我修改为数据模型类，我自己还是先使用字典。同时，数据模型有一个问题就是即使用不到某个key也会生成，因此导致信息传递不明确

## 疑惑
目前有一个问题在于数据配方经过Detector Presenter这些处理之后，变为了其他的数据包，如果我想要携带东西就需要一环一环更新——但这也是它的设计理念没错
好像甚至都不用给Intervention一个配方，一个id就足够了
- 在这里，我需要让Intervention展示一个标题和一些选项，我需要定义的是什么？感觉有点复杂啊。要不然就不管选项数量定义，直接在Narrative中修改，写了多少就有多少个选项，我觉得可以。但需要给选项上一个类别。其实我觉得Intervention可以做类似card的，但是好像有点麻烦
