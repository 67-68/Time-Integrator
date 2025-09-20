import sys

from ti.core.App import TimeIntegrator



if __name__ == "__main__":
    integrator = TimeIntegrator()
    integrator.mainWindow.show()        # 显示主窗口
    sys.exit(integrator.app.exec())     # 进入 Qt 事件循环


# contract被重置了，或许是因为重新加载了卡片和contract5