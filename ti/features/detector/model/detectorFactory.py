from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.core.Interfaces.model.repository_interface import IRepository
from ti.features.detector.model.model import Detector_Recipe, Detector_Recipe_ID
from ti.features.detector.service.matcher_resolver import MatcherResolver
from ti.model.yaml_repository import YamlRepository
from ti.services.symbol_service import SymbolService, factory_dependency_check


class DetectorFactory:
    def __init__(
        self,
        repository: YamlRepository,
        symbol_service: SymbolService
        ):
        """_summary_
        这个类负责创建所有的Detector实例
        它有一个函数接受ID
        按需创建Detector
        它从Repository获取配方
        """
        self.repository = repository
        self.symbol_service = symbol_service
        # 缓存现在通过YamlRepository管理，不再需要单独的缓存服务
        
    def appoint_cache(self, cache: type[IRepository]):
        # 缓存现在通过YamlRepository管理，不再需要单独的缓存服务
        pass
    
    def appoint_repository(self, repository: type[IRepository]):
        self.repository = repository
        
    @factory_dependency_check('repository')
    def create_detector(
        self,
        id,
    ) -> type[DetectorInterface]:
        """_summary_
        输入一个Detector_Recipe_ID Enum类作为ID
        返回一个Detecotr实例
        Args:
            id (Detector_Recipe_ID): _description_
        """
        
        # 获取recipe_id
        recipe_id = id.value if hasattr(id, 'value') else id
        
        # 从YamlRepository获取配方数据
        recipe_data = self.repository.get_by_id(recipe_id)
        if not recipe_data:
            raise ValueError(f"Recipe not found for id: {recipe_id}")
        
        # 使用detector_id作为card_type_id
        recipe_data.config.card_type_id = recipe_id
        
        # 解析detector类字符串到实际的类
        detector_class = self.symbol_service.resolve_component_class(recipe_data.detector, "detector")
        config = recipe_data.config
        
        # 使用matcher resolver解析配置中的matcher字符串
        matcher_resolver = MatcherResolver()
        config = matcher_resolver.resolve_config(config)
        
        # 不再需要缓存服务参数
        detector = detector_class(config)
        
        return detector