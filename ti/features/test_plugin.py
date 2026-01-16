from PyQt6.QtWidgets import QVBoxLayout, QLabel
from ti.model.core_pages import CoreView
from ti.model.plugin.page_contributions import PageContribution
from ti.model.plugin.page_extension_interface import IPageExtension
from ti.view.BasicWidget import BasicWidget

class TestPlugin(IPageExtension):
    def __init__(self):
        super().__init__()
        
    def initialize(self, eventBus):
        eventBus.publish("PagePluginRegistered", self.page_contributions)
        
    @property
    def name(self):
        return "test"
    
    
    def shutdown(self):
        return super().shutdown()
    
    @property
    def page_contributions(self):
        parent_page = CoreView.SETTING_PAGE.value
        page_id = "test_view"
        navigation_name = "开始测试"
        
        test_pl = PageContribution(
            page_id,
            navigation_name,
            parent_page,
            create_page_callback=self.create_page
        )
        
        page_contributions = [test_pl]
        
        return page_contributions
    
    def create_page(self, page_id):
        """创建指定页面"""
        return self._create_test_page()

    def _create_test_page(self):
        view = BasicWidget()

        # Create main layout
        main_layout = QVBoxLayout(view)

        # Create a context container similar to TimelineView
        container_widget = BasicWidget()
        container_layout = QVBoxLayout(container_widget)
        container_widget.setStyleSheet("background-color: #e6f3ff; border-radius: 5px; padding: 10px; margin: 5px;")

        # Add title
        title_label = QLabel("Context: Work Session")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        container_layout.addWidget(title_label)

        # Add some action units (simulated)
        action_styles = [
            ("Meeting", "#d4edda"),
            ("Coding", "#fff3cd"),
            ("Break", "#f8d7da")
        ]

        for action_name, color in action_styles:
            action_widget = BasicWidget()
            action_layout = QVBoxLayout(action_widget)
            action_widget.setStyleSheet(f"background-color: {color}; border-radius: 3px; padding: 5px; margin: 2px;")
            action_label = QLabel(f"Action: {action_name}")
            action_layout.addWidget(action_label)
            container_layout.addWidget(action_widget)

        # Add the container to main layout
        main_layout.addWidget(container_widget)

        # Add another context container with different color
        container2 = BasicWidget()
        container_layout2 = QVBoxLayout(container2)
        container2.setStyleSheet("background-color: #fff0e6; border-radius: 5px; padding: 10px; margin: 5px;")

        title_label2 = QLabel("Context: Personal Time")
        title_label2.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 5px;")
        container_layout2.addWidget(title_label2)

        personal_actions = [
            ("Exercise", "#e6f3ff"),
            ("Reading", "#f0e6ff")
        ]

        for action_name, color in personal_actions:
            action_widget = BasicWidget()
            action_layout = QVBoxLayout(action_widget)
            action_widget.setStyleSheet(f"background-color: {color}; border-radius: 3px; padding: 5px; margin: 2px;")
            action_label = QLabel(f"Action: {action_name}")
            action_layout.addWidget(action_label)
            container_layout2.addWidget(action_widget)

        main_layout.addWidget(container2)

        return view
        