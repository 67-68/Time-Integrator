这个文档用来解释这个服务怎么运转

它的职责是解析用户的行动并给出presenter需要执行的函数
它接受一个RawUserAction Enum类
它会结合ActionUnit来判断是否是什么意图

例如，如果RawUserAction = "EnterPressed"
那么它就会返回保存数据的指令

它返回的指令是command dataclass, 看起来像是这样


class ICommand(ABC):
    @abstractmethod
    def execute(self): ...

这个类是所有command命令类的父类和接口

具体的command看起来像是这样

1. 情况1: 使用接口定义需要执行的方法

@dataclass
class UpdatePropertyViewCommand(ICommand):
    # 命令在被创建时，就携带了它执行所需要的所有“弹药”
    view_to_update: IPropertyView # 依赖于接口
    data_to_fill: dict

    def execute(self):
        print("Executing: UpdatePropertyViewCommand")
        self.view_to_update.fill_data(self.data_to_fill)

也就是说，它使用一个接口来定义需要返回的命令
在presenter接收返回值的时候，可以直接执行命令

2. 情况2: 在presenter内使用一个哈希表查找命令所对应的函数，本地执行

一个保存数据的命令看起来像是：

> in presenter
self.intent_handlers = {
    "SAVE_REQUESTED": self._handle_save_request,
    "UPDATE_UI": self._handle_ui_update,
}

def _on_user_action(...):
    intent = self.service.decide(...)
    handler = self.intent_handlers.get(intent.command_type)
    if handler:
        handler(intent.data)

def _handle_save_request(self, data):
    # 我只负责把它包装成一个更高级的事件，然后发出去
    self.bus.publish(SaveRequestCommand(data=data))

> in command.py

@dataclass
class SaveDataCommand(ICommand):
    command_type: "SAVE_REQUESTED"
    view_to_update: IPropertyView # 依赖于接口
    data: ActionUnit

    def execute(self):
        self.view_to_update.fill_data(self.data_to_fill)

