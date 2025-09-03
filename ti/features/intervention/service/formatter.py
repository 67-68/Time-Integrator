from ti.features.intervention.model.model import INVState
from ti.features.intervention.model.narratives import InterventionNarrator
from ti.services.utils import randomChoser


class INV_Formatter:
    def __init__(
        self,
        IN: InterventionNarrator
    ):
        self.IN = IN
    
    def format(
        self,
        intervention_id: str,
        state_key: str
        ) -> dict:
        """
        重写后的format方法，用于格式化并提供一个完整状态所需的所有文本。
        它会从Narrative中获取标题和所有按钮的文本，并处理随机选择逻辑。
        
        Args:
            intervention_id (str): 干预的ID.
            state_key (str): 当前状态的键名 (e.g., "init").

        Returns:
            dict: 一个包含格式化后文本的字典，结构如下:
                  {
                      "title": "选择后的标题文本",
                      "buttons": {
                          "event_id_1": "按钮1的文本",
                          "event_id_2": "按钮2的文本"
                      },
                      "id": "干预ID",
                      "state": "状态键名"
                  }
        """
        # 1. 首先通过Narrator获取对应ID和状态的所有文本数据
        narration_data = self.IN.get_text_by_id(intervention_id, state_key)
        
        # 2. 从数据中获取 "presentation" 部分
        presentation_data = narration_data["presentation"]

        # 3. 格式化标题
        # 获取标题列表并随机选择一个
        title_options = presentation_data["title"]
        formatted_title = randomChoser(title_options)
        
        # 4. 格式化所有按钮
        formatted_buttons = {}
        button_options_data = presentation_data["button"]
        
        for btn_id, text_or_list in button_options_data.items():
            # 复用与 format_btn 相同的逻辑来处理单个按钮的文本
            if isinstance(text_or_list, list):
                # 如果是列表，随机选择一个
                formatted_buttons[btn_id] = randomChoser(text_or_list)
            else:
                # 如果是字符串，直接使用
                formatted_buttons[btn_id] = text_or_list
        
        # 5. 组装并返回最终的数据包
        pack = {
            "title": formatted_title,
            "buttons": formatted_buttons, # 使用 "buttons" 作为键名更清晰
            "id": intervention_id,
            "state": state_key
        }
        
        return pack
    
    def format_btn(
        self,
        INV_ID: str,
        state_key: str,
        btn_id: str
    ):
        """
        这个函数通过ID获取并格式化单个按钮的文本。
        它从Narrative中获取数据，并处理文本可能是列表的情况（随机选择其一）。
        """
        # 1. 通过 narrator 获取对应干预和状态的所有文本数据
        narration_data = self.IN.get_text_by_id(INV_ID, state_key)
        
        # 2. 从数据中定位到所有按钮的文本定义
        button_texts = narration_data["presentation"]["button"]
        
        # 3. 根据传入的 btn_id 找到对应的文本（可能是字符串或列表）
        target_text = button_texts[btn_id]
        
        # 4. 为了与 format 方法的行为保持一致，如果文本是列表，则随机选择一个
        #    如果只是字符串，则直接返回。
        #    这增加了灵活性，可以让同一个按钮有多种不同说法。
        if isinstance(target_text, list):
            return randomChoser(target_text)
        else:
            return target_text