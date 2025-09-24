from ti.core.Interfaces.model.yaml_repository_interface import IYamlRepository


class INVRecipeRepository(IYamlRepository):
    def __init__(self):
        super().__init__()
        
    def delete(self, id):
        return super().delete(id)
    
    def save(self):
        return super().save()
    
    def load(self):
        return super().load()
    def get_all(self) -> list[INVProjectReicpe]:
        return super().get_all()
    def get_by_id(self, id):
        return super().get_by_id(id)
    
    @property
    def file_path(self):
        return "ti/features/refactored_intervention/model/inv_recipe.yaml"
    
    