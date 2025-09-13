InsightPlugin 在被请求时，延迟创建并组装出InsightPresenter和InsightView。
InsightPresenter 被激活（比如，用户切换到这个页面）。
它的唯一职责，是调用**CardGenerationService.generate_todays_insights()**。
CardGenerationService (新的核心) 开始工作：
a. 它调用**RecipeProvider.get_recipes_for_today()，获取所有相关的配方。
b. 它遍历这些配方。
c. 在循环内部，它维护一个“Generator策略字典”，根据recipe.type，选择一个具体的Generator（比如ConditionalCardGenerator）。
d. 它调用generator.generate_raw_data(recipe)，得到未格式化的卡片数据模型。
e. 它立刻将这份raw_data，交给CardFormattingService（它内部也维护着一个“Narrative库策略字典”），得到格式化好**的ViewModel。
CardGenerationService 将一个完整的List[InsightCardViewModel]，返回给InsightPresenter。
InsightPresenter 接收到这份最终的、可直接展示的ViewModel列表。
它调用**self.view.display_insights(view_models)**。
InsightView 接收到ViewModel列表，并使用一个**CardFactory**，将它们循环渲染成一个个TrendCard QWidget，并添加到自己的布局中。