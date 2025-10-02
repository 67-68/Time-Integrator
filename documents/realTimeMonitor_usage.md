# RealTimeMonitor 使用文档

## 概述

RealTimeMonitor 是一个实时行为模式监控系统，用于检测用户行为数据中的特定模式，并在模式匹配时触发干预事件。

## 核心概念

### Monitor_Pack 监控包

```python
@dataclass
class Monitor_Pack:
    id: str          # detector recipe ID (必须存在于DetectorRepository中)
    monitor_id: str  # monitor标识符 (用于事件发布和监控管理)
    hook: list[Matcher]  # 匹配器列表，定义要监控的行为模式
```

### Thread_Pack 线程包

```python
@dataclass
class Thread_Pack:
    monitors: dict[str, Monitor_Pack]  # monitor_id -> (Monitor_Pack, Detector)
    thread_factory: DetectorFactory     # 该线程的detector工厂
    thread_id: str                      # 线程标识符
```

## 主要方法

### 1. 创建监控线程

```python
def create_thread(self, thread_id: str, detector_factory: DetectorFactory) -> str
```

**功能**: 创建一个新的监控线程

**参数**:
- `thread_id`: 线程唯一标识符
- `detector_factory`: 用于创建detector的工厂实例

**示例**:
```python
monitor.create_thread("post_eat_waste", detector_factory)
```

### 2. 添加监控项目到线程

```python
def add_monitor_to_thread(self, thread_id: str, monitor_pack: Monitor_Pack)
```

**功能**: 向指定线程添加监控项目

**参数**:
- `thread_id`: 目标线程ID
- `monitor_pack`: 监控包配置

**示例**:
```python
pack = Monitor_Pack(
    id="post_eat_waste",           # detector recipe ID
    monitor_id="post_eat_waste_source",  # monitor标识符
    hook=[matcher.action_is("吃饭")]     # 匹配器列表
)
monitor.add_monitor_to_thread("post_eat_waste", pack)
```

### 3. 移除监控项目

```python
def remove_monitor_from_thread(self, thread_id: str, monitor_id: str)
```

**功能**: 从线程中移除指定的监控项目

**参数**:
- `thread_id`: 线程ID
- `monitor_id`: 监控项目ID

### 4. 获取线程列表

```python
def list_threads(self) -> list[str]
```

**功能**: 返回所有活跃线程的ID列表

### 5. 获取线程监控项目

```python
def get_thread_monitors(self, thread_id: str) -> dict[str, tuple[Monitor_Pack, BaseDetector]]
```

**功能**: 获取线程中所有监控项目及其对应的detector

## 使用流程

### 1. 初始化监控系统

```python
from ti.services.realTimeMonitor import RealTimeMonitor, Monitor_Pack
from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.service.matchers import Matcher

# 创建监控器实例
monitor = RealTimeMonitor(data_service, event_bus)

# 创建detector工厂
detector_factory = DetectorFactory(detector_repository)
```

### 2. 创建监控线程

```python
# 为每个干预项目创建独立的线程
monitor.create_thread("post_eat_waste", detector_factory)
```

### 3. 配置监控项目

```python
matcher = Matcher()

# 定义监控包
pack = Monitor_Pack(
    id="post_eat_waste",           # 必须存在于DetectorRepository中
    monitor_id="post_eat_waste_source",  # 唯一标识符
    hook=[
        matcher.action_is("吃饭"),
        matcher.duration_is_greater_than(10)
    ]
)

# 添加到线程
monitor.add_monitor_to_thread("post_eat_waste", pack)
```

### 4. 事件处理

当模式匹配时，RealTimeMonitor会发布事件：
- 事件名称: `{thread_id}_{monitor_id}_pattern_detected`
- 事件数据: `(thread_id, monitor_id)`

**订阅事件示例**:
```python
def handle_pattern_detected(data):
    thread_id, monitor_id = data
    print(f"线程 {thread_id} 的监控项目 {monitor_id} 检测到模式")

event_bus.subscribe("post_eat_waste_post_eat_waste_source_pattern_detected", 
                    handle_pattern_detected)
```

## 最佳实践

1. **线程设计**: 为每个独立的干预项目创建单独的线程
2. **ID命名**: 使用有意义的ID命名，便于调试和维护
3. **错误处理**: 确保detector recipe ID存在于DetectorRepository中
4. **资源清理**: 使用完成后及时移除监控项目

## 常见问题

### Q: monitor_id和detector_id有什么区别？
A: 
- `detector_id`: 用于查找detector配方的ID，必须存在于DetectorRepository中
- `monitor_id`: 监控项目的唯一标识符，用于事件发布和监控管理

### Q: 如何调试模式检测问题？
A: 检查RealTimeMonitor的输出日志，确认：
1. 线程是否正确创建
2. 监控项目是否成功添加
3. 事件是否正确发布

### Q: 如何处理多个相似的监控项目？
A: 使用不同的monitor_id但相同的detector_id，这样可以复用detector配方但独立管理每个监控项目。