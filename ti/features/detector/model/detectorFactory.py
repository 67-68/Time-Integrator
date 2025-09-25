from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.core.Interfaces.model.repository_interface import IRepository
from ti.features.insight.service.insightCacheService import InsightCacheService
from ti.features.detector.model.detectorRepository import DetectorRepository
from ti.features.detector.model.model import Detector_Recipe, Detector_Recipe_ID
from ti.features.yaml_database.service.yaml_parser_service import YamlParser


class DetectorFactory:
    def __init__(
        self,
        repository: DetectorRepository,
        yaml: YamlParser
        ):
        """_summary_
        这个类负责创建所有的Detector实例
        它有一个函数接受ID
        按需创建Detector
        它从Repository获取配方
        """
        self.repository = repository
        self.cache = InsightCacheService(yaml) #我不管了...
        
    def appoint_cache(self,cache: type[IRepository]):
        self.cache = cache
    
    def appoint_repository(self,cache: type[IRepository]):
        self.cache = cache
        
    def create_detector(
        self,
        id,
        card_type_id,
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
            recipe: Detector_Recipe = self.repository.get_recipe_by_id(id)

            # 赋予这个Detector配方类卡片ID
            recipe.config.card_type_id = card_type_id # 这tm是啥
            
            detector_category = recipe.detector
            config = recipe.config
            
            detector = detector_category(config,self.cache)
            
            return detector
        except Exception as e:
            print("=" * 50)
            print("DETECTOR FACTORY ERROR! check if use unmatch repository and cache!")
            print("=" * 50)