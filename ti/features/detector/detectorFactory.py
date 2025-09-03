from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.services.dataAccess.insightCacheService import InsightCacheService
from ti.features.detector.detectorRepository import DetectocRepository
from ti.features.detector.model import Detector_Recipe, Detector_Recipe_ID


class DetectorFactory:
    def __init__(
        self,
        repository: DetectocRepository,
        ICS: InsightCacheService
        ):
        """_summary_
        这个类负责创建所有的Detector实例
        它有一个函数接受ID
        按需创建Detector
        它从Repository获取配方
        """
        self.repository = repository
        self.ICS = ICS
        
    def create_detector(self,id,card_type_id) -> type[DetectorInterface]:
        """_summary_
        输入一个Detector_Recipe_ID Enum类作为ID
        返回一个Detecotr实例
        Args:
            id (Detector_Recipe_ID): _description_
        """
        recipe: Detector_Recipe = self.repository.get_recipe_by_id(id)

        # 赋予这个Detector配方类卡片ID
        recipe.config.card_type_id = card_type_id
        
        detector_category = recipe.detector
        config = recipe.config
        
        detector = detector_category(config,self.ICS)
        
        return detector
        
        