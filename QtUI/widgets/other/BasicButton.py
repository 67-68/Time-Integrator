from PyQt6.QtWidgets import QToolButton

class BasicButton(QToolButton):
    def __init__(self, master = None, **kwargs):
        super().__init__(master,**kwargs)
        
        self.setMinimumWidth(100)
        
        #  ------ 设置外部传入参数的检测 ------    
        if 'text' in kwargs:
            self.setText(kwargs['text'])
        if 'clicked' in kwargs and callable(kwargs['clicked']):
            self.clicked.connect(kwargs['clicked'])