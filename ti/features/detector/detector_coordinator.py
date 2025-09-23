from ti.features.detector.model.detectorFactory import DetectorFactory
from ti.features.detector.model.detectorRepository import DetectocRepository
from ti.features.detector.model.model import Detector_Recipe_ID
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.services.sessionCache import SessionCache


class DetectorCoordinator:
    def __init__(self, repository: DetectocRepository = None, cache: SessionCache = None):
        """
        Detector协调器，通过插件系统提供detector实例
        """
        if repository is None:
            self.repository = DetectocRepository(YamlParser())
        else:
            self.repository = repository
            
        if cache is None:
            self.cache = SessionCache()
        else:
            self.cache = cache
            
        self.factory = DetectorFactory(self.repository, self.cache)
    
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
            detector = self.factory.create_detector(detector_id_enum, detector_id)
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
    
    def get_repository(self) -> DetectocRepository:
        """
        获取detector仓库实例
        
        Returns:
            DetectocRepository: detector仓库
        """
        return self.repository