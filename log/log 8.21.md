## 进展
- 在definitions文件中添加了新的状态ENum类
- 在Narratives文件中修改了文件结构
- 修改了InterventionService中Presenter创建
- 修改了InterventionCard创建，让其可以携带数据流state
- 修改了Formatter, 建立为服务
- 修改了Analysis Page, 数据流
- ServiceContainer加入新的服务
- 修改了InterventionPresenter, 处理事件展示选择选项之后的回复
- 让ai创建了两张图，在[2]
其实就是改了一堆数据流，我迫切需要一张图来给我指示一下数据流传递
一个好的数据流会让我受益终身QwQ

## 思考
我在处理InterventionPresenter和其ui子类的交互问题，ui的每一个事件都要上传到这个类来处理，因此我应该做的是首先识别出ui有什么行动，然后接受
鉴于它是在ui被选择之后创建的，它的第一个事件应该在它创建之后立即被传入和处理