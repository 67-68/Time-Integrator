from Core.dataAccess.dataManager import updateDataKey
from QtUI.App import TimeIntegrator
import sys

DEBUG_UI = True


if __name__ == "__main__":
    integrator = TimeIntegrator()
    integrator.connectSignal()          # 建立 Presenter 与 View 的信号
    integrator.initialization()
    integrator.mainWindow.show()        # 显示主窗口
    sys.exit(integrator.app.exec())     # 进入 Qt 事件循环


