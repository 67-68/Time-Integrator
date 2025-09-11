from PyQt6.QtWidgets import QApplication
import sys
from ti.features.core_capture.CapturePage import New_CapturePage
from ti.presenters.capture_page_presenter import CapturePagePresenter
from ti.view.views import SettingPage
from ti.services.analysis.otherAnalysis import updateActionList
from ti.services.dataAccess.dataService import DataService
from ti.view.views.MainWindow import MainWindow
from ti.core.mainCoordinator import MainCoorinator
from ti.core.definitions import TODAY
# from ti.presenters.menuPresenter import MenuPresenter
from ti.services.realTimeMonitor import RealTimeMonitor
from ti.services.serviceContainer import ServiceContainer
from ti.services.utils import load_qss, log_message

log_message("Application starting...")

class TimeIntegrator:
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #  ---------- 初始化 ----------
        #  ----- 创建应用实例 ------
        self.app = QApplication(sys.argv)
        # self.menuPresenter = MenuPresenter()
        
        #  ------ 创建UI ------
        self.mainWindow = MainWindow()
        
        styleSheet = load_qss()
        self.app.setStyleSheet(styleSheet)
        self.ui = self.mainWindow.getUIs()
        self.ui["MW"] = self.mainWindow
        
        
        
        #  ------ 创建所有的服务实例 ------
        self.services = ServiceContainer()
        self.dataService: DataService = self.services.getService("DS")
        
        self.bus = self.services.getService("bus")
        self.capture_page = New_CapturePage(self.mainWindow)
        self.presenter = CapturePagePresenter(self.capture_page, self.bus)
        
        self.coordinator = MainCoorinator(self.services,self.ui)
        
        #  ------ 持有的状态 ------
        self.createState()
                        
        #  ------ 连接信号和槽 ------
        self.connectSignal()
        
        #  ------ 初始化，传递依赖 ------
        self.refreshWidget()
        
        #  ------ 初始化今天 -----
        self._on_date_selected(TODAY)
    
        

    """ ------------------------------ Basic functions ------------------------------"""    
    def connectSignal(self):
        self.mainWindow.timeSpan_choosed.connect(self._on_Time_Choosed)
        self.mainWindow.saveData_button_clicked.connect(lambda f:self._on_saveButton_clicked(f))
        self.mainWindow.date_selected.connect(self._on_date_selected)
        self.mainWindow.list_item_selected.connect(self._on_list_item_selected)
        self.mainWindow.new_button_selected.connect(self.createNewRecord)
        
        # 连接测试新capture page的信号
        self.mainWindow.SP.test_new_capture_page.connect(self.test_create_capture_page)
    
    def createState(self):
        self.isDebugMode = False
        self.currentDate = None
        self.currentActionUnit = None 
        self.previousAU = None
        
        self.SP: SettingPage = self.mainWindow.getUI("SP")
        self.AP = self.mainWindow.getUI("AP")
        
        self.monitor: RealTimeMonitor = self.services.getService("RTM")
    
    def createNewRecord(self):
        """
        这个函数用来创建新的记录
        新的记录不会被保存到正式的数据状态中
        直到它被保存
        """
        self.previousAU = self.currentActionUnit
        
        nR = self.dataService.createNewData()
        nR.date = self.currentDate
        self.currentActionUnit = nR
        #新数据暂时不放进总的数据中，等到修改之后再检测
        
        self._on_list_item_selected(nR)
        
    def _on_list_item_selected(self,data):
        """
        这个函数用来更新
        当QlistWidget被选中的时候
        """
        self.previousAU = self.currentActionUnit
        #把新数据放上去
        
        self.currentActionUnit = data
        
        # 更新 CapturePage，使编辑区与新选中的 actionUnit 同步
        self.mainWindow.switchCPData(data)
        
    def _on_saveButton_clicked(self,actionUnit):
        self.saveData(actionUnit)

    def saveData(self,actionUnit):
        """
        保存一条数据
        准确来说，是修改原本的数据
        把相同uid的数据叠加上去
        （同时，保存之前的数据状态)
        """
        date = self.currentDate
        actionUnit.date = date
        # 这里的id没有必要，因为新建的时候就有了id
                
        updateActionList(actionUnit)
        self.dataService.add_actionUnit(actionUnit)
        
        
        self.refreshWidget()         #初始化
        self.mainWindow.fillCPData(self.dataService.get_data()[date],self.currentActionUnit)
        self.mainWindow.switchCPData(self.currentActionUnit)
    
    #UNIVERSAL; INPUT Str timeChoosed; OUTPUT the data that should update
    def _on_Time_Choosed(self,newTimeChoosed):
        actionUnits = getActionUnit(newTimeChoosed)
        if not actionUnits:
            return
        self.mainWindow.updateMenu(self.menuPresenter.processData(actionUnits))

    def _on_date_selected(self,date):
        data = self.dataService.get_date_data(date)
        self.currentDate = date
        
        data = sorted(data, key=lambda au: au.get("start", ""))
        if data: 
            self.currentActionUnit = data[0] 
        else:
            self.currentActionUnit = self.dataService.createNewData()
            print("initializing...no data today")
                
        self.mainWindow.fillCPData(data,self.currentActionUnit)
    
    def refreshWidget(self): 
        """_summary_
        初始化，传递依赖，刷新所有需要数据的功能
        """    
        #  --- 传递依赖 ---
        # se-lf.mainWindow.initialization(self.dataService.get_data())
        pass

    
    def test_create_capture_page(self):        
        # 添加到mainWindow的stacked widget中
        self.mainWindow.MW.stackedWidget.addWidget(self.capture_page)
        
        # 存储引用
        self.ui["NewCP"] = self.capture_page
        
        # 切换到新的capture page
        self.mainWindow.MW.stackedWidget.setCurrentWidget(self.capture_page)