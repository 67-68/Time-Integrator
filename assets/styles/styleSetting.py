from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QWidget
from PyQt6.QtGui import QColor

def apply_shadow(widget: QWidget):
    """
    为一个控件应用一个标准的、现代感的阴影效果。
    这个函数在Python代码中调用，而不是在QSS中。
    """
    shadow_effect = QGraphicsDropShadowEffect()
    
    # 设置阴影的关键属性
    shadow_effect.setBlurRadius(15)  # 阴影的模糊半径，数值越大越模糊、越扩散
    shadow_effect.setColor(QColor(0, 0, 0, 80)) # 阴影颜色。使用带透明度的黑色(rgba)是关键
    shadow_effect.setOffset(0, 4)    # 阴影的偏移量。(x, y)，正y值表示向下偏移
    
    # 将效果应用到控件上
    widget.setGraphicsEffect(shadow_effect)