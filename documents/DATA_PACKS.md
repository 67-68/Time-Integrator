## 1. insight_pack
- **来源**: Detector
- **送给**: InsightEngine
- **用途**: 给presenter, 制作成为presenter_pack
- **包括**: {
    - weight: 重要程度
    - data: 所有匹配的au
    - id: 模式id
    - intervention: 可选干涉数据
}
- **详细说明**: 这个数据包是被detector收集，专门用来给presenter制作的
    - weight: 它是这张卡片的重要程度，会被用来在"所有相同类型模式的卡片"中排序
    - data: 所有匹配的行动单元，使用字典结构
    - id: 模式的id，类似"eat_then_sleep"
    - intervention: 可选的干涉数据，用于干预功能

## 2. present_pack
- **来源**: Presenter
- **送给**: InsightEngine -> Formatter
- **用途**: 给formatter, 制作成为card_pack, 卡片可以直接使用
- **包括**: {
    - card_type: 卡片的外观类型
    - judgement_key: 卡片的价值判断
    - sementic_key: 卡片的数据展示
    - data: 卡片的数据
    - id: 模式id
    - weight: 重要程度
    - intervention: 可选干涉数据
}
- **详细说明**: 这个数据包是被presenter从insight_pack修改来，供formatter使用的
    - card_type: 卡片外观的类型（警告、成功、信息等）
    - judgement_key: 卡片的价值判断文本键
    - sementic_key: 卡片的数据展示文本键
    - data: 扁平化的卡片数据
    - weight: 重要程度，用于卡片排序
    - intervention: 可选的干涉数据

## 3. card_info_pack
- **来源**: InsightEngine
- **送给**: InsightEngine内部使用
- **用途**: 存储卡片相关信息
- **包括**: {
    - detector: 检测器对象
    - id: 卡片id
    - presenter: presenter函数
}
- **详细说明**: 用于在InsightEngine内部管理卡片配置

## 4. recipe_pack
- **来源**: card_recipe.py
- **送给**: InsightEngine
- **用途**: 定义卡片生成配方
- **包括**: {
    - id: 配方id
    - analyzer/presenter/detector: 处理函数
    - config: 配置信息
    - duration: 时间范围
}
- **详细说明**: 定义如何生成和分析卡片

## 5. action_unit_pack
- **来源**: DataService
- **送给**: InsightEngine
- **用途**: 基本数据处理单元
- **包括**: {
    - start_time: 开始时间
    - end_time: 结束时间
    - category: 类别
    - metadata: 附加数据
}
- **详细说明**: 行动单元是时间分析的基本单位