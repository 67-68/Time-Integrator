from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.core.Interfaces.model.repository_interface import IRepository
from ti.features.insight.service.insightCacheService import InsightCacheService
from ti.features.detector.model.model import Detector_Recipe, Detector_Recipe_ID
from ti.model.yaml_repository import YamlRepository
from ti.services.symbol_service import SymbolService


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
        self.cache = InsightCacheService() #我不管了...
        
    def appoint_cache(self,cache: type[IRepository]):
        self.cache = cache
    
    def appoint_repository(self,cache: type[IRepository]):
        self.cache = cache
        
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
        if not hasattr(self,"repository") or not hasattr(self,"cache"):
            print("=" * 50)
            print("DETECTOR FACTORY ERROR! please appoint cache and repository!")
            print("=" * 50)
            
            raise ValueError("Repository or cache not initialized")
        
        try:    
            # 获取recipe_id
            if hasattr(id, 'value'):
                recipe_id = id.value
            else:
                recipe_id = id
            
            # 从YamlRepository获取配方数据
            recipe_data = self.repository.get_by_id(recipe_id)
            if not recipe_data:
                raise ValueError(f"Recipe not found for id: {recipe_id}")
            
            # 使用detector_id作为card_type_id
            recipe_data.config.card_type_id = recipe_id
            
            # 解析detector类字符串到实际的类
            detector_class = self.symbol_service.resolve_symbol("detector", recipe_data.detector)
            config = recipe_data.config
            
            detector = detector_class(config, self.cache)
            
            return detector
        except Exception as e:
            print("=" * 50)
            print("DETECTOR FACTORY ERROR! check if use unmatch repository and cache!")
            print(f"Error: {e}")
            print("=" * 50)
            raise