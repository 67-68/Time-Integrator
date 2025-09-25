from ti.core.eventBus import EventBus
from ti.features.detector.model.detectorRepository import DetectorRepository
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
        detector_repository: DetectorRepository,
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
        recipes: list[INVProjectRecipe] = self.recipe_repository.get_all()
        projects = {}
        
        if not recipes:
            return
        
        for recipe in recipes:
            event_source_instances = self._create_event_sources(recipe)
            view_instances = self._create_views(recipe)
            
            projects[recipe.project_id] = INVProjects(
                event_source_instances,
                view_instances,
                recipe.project_id
            )
        
        return projects

    def _create_event_sources(self, recipe: INVProjectRecipe) -> dict[str, INVActionEventSource]:
        """Create event source instances for a recipe"""
        event_source_instances = {}
        
        for event_source_id, event_source_recipe in recipe.event_sources.items():
            class_name = event_source_recipe.class_name
            rule = event_source_recipe.rule
            
            # 使用SymbolService解析类名
            es_class = self.symbol_service.get_symbol(class_name)
            
            if issubclass(es_class, INVActionEventSource):
                event_source_instance = es_class(self.detector_repository, self.monitor)
                event_source_instance.initialize(recipe.project_id, self.bus, rule)
                event_source_instances[event_source_id] = event_source_instance
        
        return event_source_instances

    def _create_views(self, recipe: INVProjectRecipe) -> dict[str, object]:
        """Create view instances for a recipe"""
        view_instances = {}
        
        for view_recipe in recipe.views:
            class_name = view_recipe.class_name
            view_rule = view_recipe.rule
            
            # 使用SymbolService解析类名
            view_class = self.symbol_service.get_symbol(class_name)
            view_id = view_rule.view_id
            view_instance = view_class(view_rule)
            view_instances[view_id] = view_instance
        
        return view_instances
        