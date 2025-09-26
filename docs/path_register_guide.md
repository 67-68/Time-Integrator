# Path Register 使用指南

## 概述

Path Register 是 Time Integrator 中用于管理符号路径的系统，它通过配置化的方式减少重复代码和错误。

## 符号在配方中的格式

### 1. 基本符号格式
- **类和方法**: `domain.symbol_name` (例如: `intervention.action_event_source`)
- **枚举**: `domain.ENUM_NAME` 或 `domain.ENUM_CLASS.ENUM_VALUE.value` (例如: `intervention.INV_VIEW_ID.POST_EAT_WASTE.value`)

### 2. 枚举符号规范
- 枚举类名必须全大写，使用下划线分隔
- 枚举值必须全大写，使用下划线分隔
- 在配方中使用时，必须包含 `.value` 后缀

### 示例
```yaml
# 正确的枚举使用
enum_reference: intervention.INV_VIEW_ID.POST_EAT_WASTE.value

# 错误的枚举使用（缺少.value）
enum_reference: intervention.INV_VIEW_ID.POST_EAT_WASTE
```

## 创建 PathRegister 的配置

### 1. 必需配置
- **domain**: 符号的域名（如 "intervention", "detector"）
- **domain_file_path**: 基础文件路径，用于确定符号文件的存放位置

### 2. 可选配置
- **enum_mapping**: 枚举映射表，用于简化枚举符号的解析

### 配置示例
```python
from ti.services.path_register_service import PathRegisterService, PathRegisterConfig

# 创建干预功能的 PathRegister
intervention_config = PathRegisterConfig(
    domain="intervention",
    domain_file_path="ti/features/intervention/model/data",
    enum_mapping={
        "INV_VIEW_ID": "inv_view_id",
        "INV_ACTION_ID": "inv_action_id"
    }
)

intervention_register = PathRegisterService(intervention_config)

# 创建检测功能的 PathRegister
detector_config = PathRegisterConfig(
    domain="detector", 
    domain_file_path="ti/features/detector/model/data"
)

detector_register = PathRegisterService(detector_config)
```

## 文件结构要求

每个 domain 需要按照以下结构组织符号文件：

```
ti/features/{domain}/model/data/
├── classes.yaml          # 类符号定义
├── class_methods.yaml    # 类方法符号定义  
├── functions.yaml        # 函数符号定义
└── enums.yaml           # 枚举符号定义
```

### 文件格式示例

**classes.yaml**
```yaml
classes:
  action_event_source:
    symbol_type: "class"
    symbol_path: "ti.features.intervention.service.inv_action_event_source.INVActionEventSource"
    symbol_domain: "intervention"
  card_view:
    symbol_type: "class" 
    symbol_path: "ti.features.intervention.presenter.inv_card_presenter.INVCardPresenter"
    symbol_domain: "intervention"
```

## 优势

1. **减少重复代码**: 不再需要为每个功能创建单独的 PathRegister 类
2. **统一配置**: 所有 PathRegister 使用相同的配置模式
3. **易于维护**: 修改配置即可调整符号解析行为
4. **错误减少**: 统一的接口减少了实现错误

## 迁移指南

从现有的具体 PathRegister 类迁移到 PathRegisterService：

1. 删除原有的 PathRegister 类文件
2. 创建相应的配置对象
3. 使用 PathRegisterService 替换原有的注册器实例
4. 确保符号文件按照规范组织