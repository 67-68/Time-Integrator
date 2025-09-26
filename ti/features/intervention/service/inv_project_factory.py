from ti.core.eventBus import EventBus
from ti.model.yaml_repository import YamlRepository
from ti.features.intervention.model.stored.inv_project_recipe import INVComponentRecipe, INVProjectRecipe, INVProjects

from ti.features.intervention.service.inv_action_event_source import INVActionEventSource
from ti.model.yaml_repository import YamlRepository
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.symbol_service import SymbolService


class INVProjectFactory:
    def __init__(
        self,
        bus: EventBus,
        monitor: RealTimeMonitor,
        detector_repository: YamlRepository,
        symbol_service: SymbolService,
        recipe_repository: YamlRepository
    ):
        self.bus = bus
        self.monitor = monitor
        self.detector_repository = detector_repository
        self.symbol_service = symbol_service
        self.recipe_repository = recipe_repository

    def create_projects(self) -> dict[str, INVProjects]:
        """
        Create all intervention projects from recipes
        Returns a dictionary mapping project_id to INVProjects
        """
        print("=" * 20)
        print("[INVFAC]Start creating recipes")
    
        recipes: list[INVProjectRecipe] = self.recipe_repository.get_all()
        projects = {}
        
        if not recipes:
            print("[INVFAC]Do not find any Recipes")
            return
        print("[INVFAC]Sucessfully Finding Recipes")
        
        for recipe in recipes:
            print(f"[INVFAC]Start creating project_recipes: {recipe.project_id}")
            event_source_instances = self._create_event_sources(recipe)
            view_instances = self._create_views(recipe)
            
            projects[recipe.project_id] = INVProjects(
                event_source_instances,
                view_instances,
                recipe.project_id
            )
            
        print("[INVFAC]End creating recipes")
        print("=" * 20)
        
        return projects
        

    def _create_event_sources(self, recipe: INVProjectRecipe) -> dict[str, INVActionEventSource]:
        """Create event source instances for a recipe"""
        event_source_instances = {}
        
        for event_source_id, event_source_recipe in recipe.event_sources.items():
            class_name = event_source_recipe.class_name
            rule = event_source_recipe.rule
            
            # 解析类名格式：domain.symbol_name 或完整路径
            if class_name.count(".") == 1:
                # 格式：domain.symbol_name
                domain, symbol_name = class_name.split(".", 1)
                # 使用resolve_symbol解析符号
                es_class = self.symbol_service.resolve_symbol(domain, symbol_name)
            else:
                # 使用get_symbol解析完整路径
                es_class = self.symbol_service.get_symbol(class_name)
            
            if issubclass(es_class, INVActionEventSource):
                event_source_instance = es_class(self.detector_repository, self.monitor)
                # 使用 symbol service 解析规则类型并创建规则对象
                rule_type_path = rule.get('rule_type')
                rule_data = rule.get('data', {})
                
                if rule_type_path:
                    # 解析规则类型
                    rule_class = self.symbol_service.get_symbol(rule_type_path)
                    if rule_class:
                        action_rule = rule_class(**rule_data)
                        event_source_instance.initialize(recipe.project_id, self.bus, action_rule)
                        event_source_instances[event_source_id] = event_source_instance
                    else:
                        print(f"Warning: Could not resolve rule type {rule_type_path}")
                else:
                    print(f"Warning: No rule_type specified for event source {event_source_id}")
        
        return event_source_instances

    def _create_views(self, recipe: INVProjectRecipe) -> dict[str, object]:
        """Create view instances for a recipe"""
        view_instances = {}
        
        for view_id, view_recipe in recipe.views.items():
            class_name = view_recipe.class_name
            view_rule = view_recipe.rule
            
            # 解析类名格式：domain.symbol_name 或完整路径
            if class_name.count(".") == 1:
                # 格式：domain.symbol_name
                domain, symbol_name = class_name.split(".", 1)
                # 使用resolve_symbol解析符号
                view_class = self.symbol_service.resolve_symbol(domain, symbol_name)
            else:
                # 使用get_symbol解析完整路径
                view_class = self.symbol_service.get_symbol(class_name)
            
            # 使用 symbol service 解析规则类型并创建规则对象
            rule_type_path = view_rule.get('rule_type')
            rule_data = view_rule.get('data', {})
            
            if rule_type_path:
                # 解析规则类型
                rule_class = self.symbol_service.get_symbol(rule_type_path)
                if rule_class:
                    view_rule_obj = rule_class(**rule_data)
                    # Create presenter with required parameters (View is created internally)
                    view_instance = view_class(
                        recipe=view_rule_obj,
                        bus=self.bus,
                        project_id=recipe.project_id,
                        view_id=view_id
                    )
                    view_instances[view_id] = view_instance
                else:
                    print(f"Warning: Could not resolve rule type {rule_type_path}")
            else:
                print(f"Warning: No rule_type specified for view {view_id}")
        
        return view_instances
        