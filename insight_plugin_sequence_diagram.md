# Insight插件UML序列图

## 洞察卡片生成流程序列图

```mermaid
sequenceDiagram
    participant App as 应用程序
    participant Plugin as InsightPlugin
    participant Coordinator as InsightCoordinator
    participant EventBus as EventBus
    participant ServiceFactory as InsightServiceFactory
    participant RecipeService as InsightRecipeService
    participant CardGenerator as InsightCardGenerator
    participant CardRenderer as InsightCardRenderer
    participant Repository as InsightCardRepository
    participant View as InsightView

    Note over App: 用户打开洞察页面
    
    App->>Plugin: create_page("insight_view")
    activate Plugin
    
    Plugin->>Plugin: create_insight_view()
    Plugin->>View: InsightView()
    activate View
    
    Plugin->>Coordinator: start_yesterday_report_generation(view)
    activate Coordinator
    
    Coordinator->>EventBus: publish(InsightCardGenerationStarted)
    
    Coordinator->>ServiceFactory: create_recipe_service()
    ServiceFactory->>RecipeService: InsightRecipeService()
    Coordinator->>RecipeService: load_recipes()
    activate RecipeService
    RecipeService-->>Coordinator: recipes
    deactivate RecipeService
    
    Coordinator->>EventBus: publish(RecipeLoaded)
    
    Coordinator->>ServiceFactory: create_card_generator()
    ServiceFactory->>CardGenerator: InsightCardGenerator()
    Coordinator->>CardGenerator: generate_cards()
    activate CardGenerator
    
    CardGenerator->>EventBus: publish(CardGenerated) for each card
    CardGenerator-->>Coordinator: cards
    deactivate CardGenerator
    
    Coordinator->>EventBus: publish(AllCardsGenerated)
    
    Coordinator->>ServiceFactory: create_card_renderer()
    ServiceFactory->>CardRenderer: InsightCardRenderer()
    Coordinator->>CardRenderer: render_cards(cards, view)
    activate CardRenderer
    
    CardRenderer->>View: add_card() for each card
    CardRenderer->>EventBus: publish(CardRendered) for each card
    CardRenderer-->>Coordinator: rendered_cards
    deactivate CardRenderer
    
    Coordinator->>EventBus: publish(InsightGenerationCompleted)
    
    Coordinator-->>Plugin: rendered_cards
    deactivate Coordinator
    
    Plugin-->>App: InsightView实例
    deactivate Plugin
    
    Note over View: 卡片显示在界面上
    
    %% 卡片保存流程
    Note over View: 用户点击保存卡片
    
    View->>EventBus: publish(SaveInsightCard)
    
    EventBus->>Repository: save_today_cards()
    activate Repository
    Repository-->>EventBus: 保存完成
    deactivate Repository
```

## 关键交互说明

### 1. 初始化阶段
- **应用程序** 调用 `InsightPlugin.create_page()`
- **插件** 创建视图并启动 `InsightCoordinator`

### 2. 配方加载阶段  
- **Coordinator** 通过工厂创建 `RecipeService`
- 加载并解析洞察卡片配方
- 发布 `RecipeLoaded` 事件

### 3. 卡片生成阶段
- **Coordinator** 通过工厂创建 `CardGenerator`
- 生成条件卡片和固定卡片
- 为每张卡片发布 `CardGenerated` 事件
- 发布 `AllCardsGenerated` 事件

### 4. 卡片渲染阶段
- **Coordinator** 通过工厂创建 `CardRenderer`
- 将卡片渲染到界面
- 为每张卡片发布 `CardRendered` 事件
- 发布 `InsightGenerationCompleted` 事件

### 5. 卡片保存阶段
- 用户操作触发 `SaveInsightCard` 事件
- **EventBus** 通知 `Repository` 保存卡片

## 架构特点

1. **事件驱动**: 每个关键步骤都发布相应事件
2. **接口依赖**: 通过工厂模式创建服务，依赖接口而非具体实现
3. **职责分离**: 每个组件职责单一明确
4. **可扩展性**: 新增卡片类型只需实现相应接口