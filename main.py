from QtUI.App import TimeIntegrator
import sys

if __name__ == "__main__":
    integrator = TimeIntegrator()
    integrator.initialization()
    integrator.mainWindow.show()        # 显示主窗口
    sys.exit(integrator.app.exec())     # 进入 Qt 事件循环


