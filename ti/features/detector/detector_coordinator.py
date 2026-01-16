from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.model.model import Detector_Recipe_ID
from ti.services.sessionCache import SessionCache
from ti.model.yaml_repository import YamlRepository
from ti.features.detector.model.model import Detector_Recipe
from ti.services.symbol_service import SymbolService


class DetectorCoordinator:
    def __init__(self, repository: YamlRepository = None, cache: SessionCache = None, symbol_service: SymbolService = None):
        """
        Detector协调器，通过插件系统提供detector实例
        """
        if repository is None:
            self.repository = YamlRepository("ti/model/data/detector_recipes.yaml", Detector_Recipe, identifier_field="recipe_id")
        else:
            self.repository = repository
            
        if cache is None:
            self.cache = SessionCache()
        else:
            self.cache = cache
            
        if symbol_service is None:
            from ti.services.symbol_service import SymbolService
            self.symbol_service = SymbolService()
        else:
            self.symbol_service = symbol_service
            
        self.factory = DetectorFactory(self.repository, self.symbol_service)
    
    def get_detector(self, detector_id: str):
        """
        根据detector_id获取detector实例
        
        Args:
            detector_id (str): detector的ID
            
        Returns:
            BaseDetector: detector实例
        """
        try:
            # 将字符串ID转换为枚举
            detector_id_enum = Detector_Recipe_ID(detector_id)
            # 使用工厂创建detector实例
            detector = self.factory.create_detector(detector_id_enum)
            return detector
        except ValueError:
            raise ValueError(f"Unknown detector ID '{detector_id}'")
    
    def get_factory(self) -> DetectorFactory:
        """
        获取detector工厂实例
        
        Returns:
            DetectorFactory: detector工厂
        """
        return self.factory
    
    def get_repository(self) -> YamlRepository:
        """
        获取detector仓库实例
        
        Returns:
            DetectorRepository: detector仓库
        """
        return self.repository