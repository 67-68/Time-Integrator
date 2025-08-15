1. 核心设计问题 (The Core Design Problem)

  在 AnalysisPage 中生成多种来源、多种逻辑的卡片时，我们面临一个核心的架构挑战：由谁来负责协调这个复杂的创建、数据管理和UI更新流程？如果将这些逻辑直接放在 AnalysisPage
  (View层) 中，会导致视图层急剧膨胀、职责不清，违反了我们MVP架构的基本原则。

  2. 架构决策 (The Architectural Decision)

  为了解决这个问题，我们引入了一个独立的 CardController 类。

  我们决策的核心是： 将“每日卡片生成”这个完整的业务功能，从 AnalysisPage 中剥离出来，封装进 CardController。它将扮演一个专职的“功能指挥官”角色。

  3. 设计理念与初始化逻辑 (Design Rationale & Initialization)

  CardController 的初始化过程，直接反映了它的核心职责。它被设计为一个“依赖注入”模式的实践者，它在创建时，需要被“注入”它完成工作所需的所有“工具”和“原材料”。

   * 为什么需要 `ServiceContainer` (服务包)?
       * 理由: CardController 的下游 Presenter (如 ConditionalCardPresenter) 需要 InsightEngine 等核心服务。CardController
         自身不应该负责创建这些全局单例服务。因此，它需要从一个更高层级的“服务容器”中获取这些服务，再“传递”给它所管理的 Presenter。这保证了服务来源的单一和架构的解耦。

   * 为什么需要 `AnalysisPage` (UI实例)?
       * 理由: CardController 的最终产出（卡片列表）必须被渲染在UI上。作为 Controller，它的职责包含了命令 `View` 进行更新。因此，它必须持有 AnalysisPage
         的引用，以便在完成所有后台工作后，能够调用 analysis_page.display_cards(...) 方法。这确保了单向的数据流：Controller -> View。

   * 为什么由它来初始化 `Presenters`?
       * 理由: ConditionalCardPresenter 和 FixedCardPresenter 是实现“卡片生成”功能的具体工作者。而 CardController 是指挥官。根据“谁使用，谁创建”的原则，CardController
         创建并管理这些 Presenter 的生命周期是其核心职责。这使得 AnalysisPage 完全不需要知道 Presenter 的存在，进一步简化了视图层的逻辑。

   * 为什么由它来提供数据?
       * 理由: 所有类型的卡片都需要基于同一份“昨日数据”。为了避免每个 Presenter 都去重复请求数据，CardController 在流程开始时，会一次性地、集中地获取昨日的所有
         ActionUnit，然后将这份统一的数据源分发给所有下游的 Presenter。这提高了效率，并保证了数据的一致性。