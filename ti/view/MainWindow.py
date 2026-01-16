from PyQt6.QtWidgets import QMainWindow
from ti.core.Interfaces.view.page_view_interface import IPageView
from ti.view.ui_rawMainWindow import Ui_MainWindow




#MVP中的view, 即用户直接看的GUI
class MainWindow(QMainWindow):
    #  ---------- 开始初始化 ----------
    def __init__(self):
        super().__init__()
        
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        
        #  --- 赋值 ---
        self.ui = {} # 存储所有界面
        
    
    def add_page(self,page: type[IPageView]):
        self.ui[page.page_name] = page
        print(f"[MainWindow]add page {page.page_name}")
        self.main_window.stackedWidget.addWidget(page)
    
    def set_page(self,page_name):
        page = self.ui[page_name]
        print(f"[MainWindow]switch to page {page.page_name}")
        self.main_window.stackedWidget.setCurrentWidget(page)
        
    def getUIs(self):
        """
        这个函数返回所有的UI实例
        包括CP, AP和MP
        """
        return self.ui
    
    def getUI(self,ui: str):
        """_summary_
        返回单个ui
        可选的有AP,CP,MP
        Args:
            ui (str): ui的名称
        """
        return self.ui[ui]
        
    def _on_page_switch_button_clicked(self,page_name):
        page = self.ui.get(page_name,"")
        if not page:
            print(f"[MainWindow]: Switching page error. Page {page_name} do not exist")
        self.main_window.stackedWidget.setCurrentWidget(page)

    

    