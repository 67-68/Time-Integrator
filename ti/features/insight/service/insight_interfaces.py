from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IInsightRecipeService(ABC):
    """洞察配方服务接口"""
    
    @abstractmethod
    def load_recipes(self) -> Dict[str, Any]:
        """加载洞察卡片配方"""
        pass


class IInsightCardGenerator(ABC):
    """洞察卡片生成器接口"""
    
    @abstractmethod
    def generate_cards(self) -> List[Any]:
        """生成洞察卡片"""
        pass


class IInsightCardRenderer(ABC):
    """洞察卡片渲染器接口"""
    
    @abstractmethod
    def render_cards(self, cards_data: List[Any], view_component: Any) -> List[Any]:
        """渲染卡片到界面"""
        pass


class IInsightServiceFactory(ABC):
    """洞察服务工厂接口"""
    
    @abstractmethod
    def create_recipe_service(self) -> IInsightRecipeService:
        """创建配方服务"""
        pass
    
    @abstractmethod
    def create_card_generator(self) -> IInsightCardGenerator:
        """创建卡片生成器"""
        pass
    
    @abstractmethod
    def create_card_renderer(self) -> IInsightCardRenderer:
        """创建卡片渲染器"""
        pass