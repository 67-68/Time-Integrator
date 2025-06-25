from PyQt6.QtWidgets import QToolButton

class BasicButton(QToolButton):
    def __init__(self, master = None, **kwargs):
        super().__init__(master,**kwargs)
        self.setStyleSheet("""
            QToolButton {
                background-color: #F4F4F4;
                border: none;
                border-radius: 0px;
                padding-top: 6px;
                padding-bottom: 6px;
                width: 100px;  /* 实际宽度由布局器和父容器决定 */
            }
            QToolButton:pressed, QPushButton:checked {
                background-color: #F4F4F4;
        """)
        
        self.setMinimumWidth(100)
        
        #  ------ 设置外部传入参数的检测 ------    
        if 'text' in kwargs:
            self.setText(kwargs['text'])
        if 'clicked' and callable(kwargs['clicked']):
            self.clicked.connect(kwargs['clicked'])
    
        