from PyQt6.QtCore import QObject

from ti.UI.views.InterventionCard import InterventionCard

class InterventionPresenter(object):
    def __init__(
        self,
        ui: InterventionCard
    ):
        """
        管理Intervention的类
        """
        self.ui = ui
        