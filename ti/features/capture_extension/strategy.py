from ti.features.capture.model.protocols.capture_renderable_item import RenderableItemModel
from ti.features.capture_extension.action_unit_list_display_renderer import ActionUnitListRenderer
from ti.model.action_unit import ActionUnit
from ti.model.action_unit_repository import ActionUnitRepository
from ti.model.yaml_repository import YamlRepository
from ti.services.dataService import DataService

# 在这个类创建组装模型

class CaptureExtensionStrategies:    
    # 要写成static
    @staticmethod
    def capture_data_model() -> RenderableItemModel:
        renderer = ActionUnitListRenderer()
        au_repo = YamlRepository(
            "model/data/dateData.json",
            ActionUnit,
            "uuid"
        )
        
        data = DataService.get_instance()
        data.add_repository(au_repo)
        
        model = RenderableItemModel(
            "action_unit",
            ActionUnit,
            renderer,
            ["list_display_presenter"],
            ["action_unit_editor"]
        )
        
        return model