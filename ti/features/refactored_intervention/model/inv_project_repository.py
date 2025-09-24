from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository
from ti.features.refactored_intervention.model.intervention_project import INVProjectModel


class INVProjectRepository(IYamlRepository):
    """
    负责保存Projects
    提供Projects获取服务
    在修改之后保存
    """
    
    
    def get_by_id(self, id) -> INVProjectModel:
        return super().get_by_id(id)
    

    def add_model(self,model: INVProjectModel):
        pass