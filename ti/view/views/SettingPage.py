from PyQt6.QtWidgets import QWidget

from PyQt6.QtCore import pyqtSignal
import uuid

from ti.view.rawUI.ui_rawSettingPage import Ui_SettingPage
from ti.view.widgets.other.BasicButton import BasicButton



class SettingPage(QWidget):
    switchPage_button_clicked = pyqtSignal(str)
    dialog_test = pyqtSignal()
    test_new_capture_page = pyqtSignal()
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.SP = Ui_SettingPage()
        self.SP.setupUi(self)
        
        self.SP.pageSwitchFrame.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))
        
        #self.SP.uidButton.clicked.connect(self.re_construct_uuid)
        
        capture_page_test_btn = BasicButton(self.SP.frame_2)
        capture_page_test_btn.setText("Test capturePage")
        self.SP.horizontalLayout.addWidget(capture_page_test_btn)
        capture_page_test_btn.clicked.connect(self.dialog_test.emit)
        
        # 添加测试新capture page的按钮
        new_capture_page_btn = BasicButton(self.SP.frame_2)
        new_capture_page_btn.setText("Test New CapturePage")
        self.SP.horizontalLayout.addWidget(new_capture_page_btn)
        new_capture_page_btn.clicked.connect(self.test_new_capture_page.emit)
        

        
        
        
        