# 简介
这个文件用来说明Intervention重构之后的架构

# 正文

## Rough Situation
(to each projects)
Every projects_recipe contain keys, when they added, the keys will automatically activated by InterventionActivater. For example, the result event of EventSource will be automaticlly direct to InterventionReducer. 

### SITUATION: Implement of a project
Rules -[Stored_In]> Repository -> Mapping -> Coordiantor

**Communication Medium And Change**: 
Rules -> Repository: yaml files(diction)
Repository: change yaml into dataclass

Repository -> Mapping: dataclasses
mapping: mapping str to class/methods

Mapping -> Coordiantor: 
coordinator: initialize them

### SITUATION: Flow of event
EventSource -> EventBus -> Reducer -[modify]> Model -> EventBus -> Presenter -[Modify]-> View

**Communication Medium And Change**: 
EventSource -> Reducer: RawEvent: The event that defined by recipe, link to special events
reducer: according to the special events(whatever the str events is), change the model

Reducer -> Model: Actions: Direct change the data inside model... or make a new one
model: store infos

Model -> Presenter: Another type of special events? or the original special events. Or publish of states?
presenter: monitor the change of model

Presenter -> View: Actions: Direct change it.
View: Showing things

### SITUATION: When View Triggered
View -> Presenter -> Eventbus -> Reducer -> Model

**Communication Medium And Change**: 
The flow of data is exactly the same as EventSource

## Core Concepts
Intervention Project: 一个代表了完整干涉生命周期的核心实体。它包含了触发规则、状态机和表现形式的配置。
Trigger: 一个可被替换的策略，负责决定何时激活一个Project。它可以是基于“实时模式”，也可以是基于“计划日程”。
Reducer: 一个纯函数，负责根据事件和当前状态，来计算一个Project的下一个状态。
View: 一个可被替换的策略，负责将一个Project的当前状态，渲染成一种具体的用户界面（模态窗口、系统通知等）。

## Detail

### Implement of Project

#### The Format of Rule
About the format, there are three class to define their behaviour: Trigger, Reducer and Presenter/View
These three class will be write into Enum class as constant.
For each of them, they should contain the class they use, and the rules for these class to implement.
The format will look like:


  




