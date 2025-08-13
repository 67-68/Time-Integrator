class Fixed_ReportGenerator():
    """_summary_
    这个类用来承载fixed card
    """
    def __init__(
        self,
        data, #需要处理的数据
        recipe: dict #固定卡片的配方
    ):
        self.data = data
        self.recipe = recipe
    
    def create_report(self) -> dict:
        """_summary_
        这个函数用来生成卡片报告
        Returns:
            dict: 处理好的卡片信息
        """
        # 创建固定卡片信息
        cardData = []
        for card in self.recipe:
            config = card["analyzer_config"]
            analyzer = card["analyzer"]
            presenter = card["presenter"]
            
            card = analyzer(self.data,config)
            card = presenter(card)

            cardData.append(card)
        
        return cardData