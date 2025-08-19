# Log for August 16, 2025

## 完成的部分
- **[BUG]** Fixed a critical bug where a single recipe could incorrectly generate multiple cards.
- **[DEBUG]** Investigated the bug by creating a dedicated unit test (`test_insight_manager.py`) to replicate the issue and validate the fix.
- **[REFACTOR]** Refactored `InsightManager` to correctly use the recipe ID for deduplication, ensuring only the highest-weighted card per recipe is returned.
- **[NOTE]** This bug was primarily resolved by the AI assistant.
- 增加了一张大的Overview,Documents/umls/0/[0]Intervention_Overview.puml

## 代办
- 把大Overview分为两张小的图，初始化图(包括整理干涉实体功能)和运行时检测图
- 开始写代码！
- 画出我承诺的那些小的图
- 把这些类添加进入Structure总类图
- 设计数据模型

## 暂存
我完成了大图，但我接下来要把它拆成两张小图，然后画一张图整理他们

