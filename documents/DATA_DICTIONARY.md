## 1.insight_pack
- **来源**: Detector

- **送给**: InsightEngine

- **用途**: 给presenter, 制作成为presenter_pack

- **包括**: {
    - weight: 重要程度
    - data: 所有匹配的au
    - history: 历史数据
    - id: 模式id
}
- **详细说明**: 这个数据包是被detector收集，专门用来给presenter制作的
    - weight: 它是这张卡片的重要程度，它通过一个或从依赖导入的重要程度算法，或使用默认的重要程度算法来计算(计算所有包括在内的au时间长度)它会被用来在“所有相同类型模式的卡片”中排序，如果生成了多张，来获取最严重的那一张，放入备选
    - data: 所有匹配的行动单元，它们不使用列表而是使用字典，key为状态的名称，长度取决于多少个状态
    - history: 历史数据，从insightCacheService中获取，专属于insight_pack包而不会被包含在另一个包内，用来生成当前卡片，在narrative中有自己对应的一个键
    - id: 模式的id，一般来说类似"eat_then_sleep", 会是模式本身的简单概括


## 2.present_pack
- **来源**: Presenter

- **送给**: InsightEngine

- **用途**: 给formatter, 制作成为card_pack, 卡片可以直接使用

- **包括**: {
    - card_type: 卡片的外观类型
    - judgement_key: 卡片的价值判断
    - sementic_key: 卡片的数据展示
    - data: 卡片的数据
    - id: 模式id
    - weight: 重要程度
}
- **详细说明**: 这个数据包是被presenter从insight_pack修改来，供formatter使用的
    - card_type: 卡片外观的类型，例如如果是警告那么就是一个感叹号，如果是展示信息就是一个Info
    - judgement_key: 卡片的价值判断，如果是鼓励就会是这个画风：“做得很棒！加油！”，同时可能存在“质疑用户记录”，“提醒用户注意”等等。对于每一个不同的模式/卡片类型，它的数据和key可能是不同的，但同样存在一些universal 的价值判断
    - sementic_key: 专注展示单纯的数据，同样，文本可能随着卡片的不同而不同，在这一部分同样会展示历史数据
    - weight: 重要程度，用来和“相同模式”的卡片相互比较，如果存在多个模式，看看谁更加重要
    - id: 卡片模式的id，类似"eat_then_waste"
    - data: 卡片的数据，原本是一个层叠的字典，但是需要使用flatten_dict函数来把它变成扁平化的字典，也是因为会不适配所以detector的数据才使用字典记录


## 3.Conditional_card_matcher
- **来源**: userMatchers.py

- **送给**: card_recipe

- **用途**: 被card_recipe中的配方使用，作为状态名称和状态匹配符(matcher)的数据来源

- **包括**: {
    - matcher: 一个简单的匹配符号，匹配所有符合的actionUnit
    - state_name: 匹配符号所对应的状态名称
}
- **详细说明**: 这个数据包是用户/系统定义的，被用来专门作为conditional_card的基石
    - matcher: 一个匹配符号，匹配符合条件的action_unit, 可以是多个matcher套娃，也可以是一个简单的matcher. 例如 action_is("sleep")
    - state_name: 状态的名称，有一定的含义，和matcher想要匹配什么高度相关，如果matcher想要匹配一个睡觉段落，那么state_name就可以是"sleep", 使用简单的字符串来定义。理论上来说可以和matcher不相关，但是最好相关。它同样会被用来在detector发现匹配模式的数据之后保存信息，作为key


## 4.Conditional_card_recipe
- **来源**: card_recipe.py

- **送给**: InsightEngine

- **用途**: 检测所有在卡组中的conditional card

- **包括**: {
    - detector: 这张卡片使用的detector, 决定了什么数据包被产出
    - config: detector的设定，决定了它怎么干
        - sequence: 不同状态的合集，决定了detector的状态和匹配
        *来源于<<data>> conditional_card_mathcer*
        - id: 卡片的id
    - presenter: 这张卡片使用的presenter,用来产出卡片外观数据包
}
- **详细说明**: 
    - detector: 它会被engine调用，对当前的actionUnit做出简单的判断，根据它被输入的config, 如果判断成功，那么进入下一个状态。如果判断不成功，那么重置所有状态，从头开始匹配。同时，它会在匹配到状态之后发出一个事件，被engine接收。*这个事件的数据包为<<data>>insight_pack*
    - config: 它决定了detector具体的状态以及名称，包括这张卡片的类比
        - sequence: 它来源于另一个matcher的数据包。正如其名字，detector会根据它的内容创建状态并依次判断是否通过。在储存数据的时候，状态名称会作为数据的key
        - id: 一般来说，它是对于这张卡片所检测的模式的一个概括性的名称，例如"post_eat_waste"检测一个在吃饭之后浪费时间的模式，同时，它表示"一类"卡片，在重要程度排序的时候会被用于分组
    - presenter: 它用来处理detector产生的数据包，给数据包添加上表示外观的，和用来和narrtive查找的key。*产生<<data>>present_pack*
