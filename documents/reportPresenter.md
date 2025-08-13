# 本文档解释关于Conditional_ReportPresenter的设计

## 设计理念
把Conditional_ReportPresenter类当作一个卡片报告功能的管理者
而非单独的Engine和Manager类来管理

也就是说，它现在不管理日期和数据，由使用它的类来管理

## 初始化
- data: 需要处理的数据
- conditional_recipe: 需要处理的条件判断卡片配方
- IE: InsightEngine, Engine实例
- IM: InsightManager, Manager实例
- fixed_recipe: dict, 需要处理的固定配方