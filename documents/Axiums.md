# Start
本文件记录其他文件提及的术语定义,以及本项目所遵守的设计哲学

## 核心工作流

目前打算根据左下角的标注，校对，修改图中标注为sequence的部分，放在左上角，如果有需要修改的数据模型和文档，放在右下角

## 术语
1. 功能本位:

> 引：什么是功能本位？基本的三类结构是什么？
这是一个被我新创造出来的词，简单来说，它是一个编程的术语，指把代码当作实现功能的工具，任何代码都是为了实现特定的功能，因此，在这个视角下，没有什么代码不是为了功能的，它们也就可以被进而分为三类，根据它们在结构上的作用来说
1. 逻辑核心
2. 上行事件
3. 下行指令

> 逻辑核心
对于逻辑核心，它指的是在一个GUI内，进行一个功能的逻辑计算，判断的那一部分，对于用户输入的奇偶性判断就在此列，它从上行的事件获取当前的情报，知道当前的情况，计算出下行的指令并返回给从属的GUI控件

它持有进行计算所必须的状态，它是，也只能是一个有状态的组件。

> 上行事件

**测试驱动开发**

**新MVP架构**

<critique>
```
@startuml

class AnalysisPage {

+ functionButton

}

class AnalysisPage_Controller {

+ _on_functionButton_clicked()

()这个函数用来写这个button被clicked 之后会发生什么

  

- services

}

AnalysisPage_Controller *-- AnalysisPage

' 这个关系正确吗？是不是反了?

  

class App {

- services: list

}

  

App o-- AnalysisPage_Controller

App o-- Other_Controllers

Other_Controllers *-- Other_UIs

  

@enduml

  

@startuml

participant "Application: app" as app

participant "AnalysisPage_Controller: Controller" as control

  

app -> control: __init__(services)

  

@enduml
```

让我用uml的语言来简单的描述一下，大概是这么个逻辑?

让我用语言对它进行进一步的描述：是否最终的结果看起来像是一张大网（天罗地网lol）覆盖在ui的地上，每一个ui的活动都需要经过这张网来表达，这张网的组成部分就是一堆的controller, 在最中心是app类？简单来说，原本我们使用一个容器类容纳ui和逻辑，现在，我们把容器类看作单纯的容器，一个工具，而不是这张事件和信号之网中的一部分？它原本的生态位被现在的controller替代了
