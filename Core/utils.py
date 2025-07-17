import datetime
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QWidget
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import QSize
import re
import os
import sys

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
    
    


def load_svg_icon(path: str, size: QSize, fill_color: QColor = None) -> QPixmap:
    """
    加载一个SVG文件，并将其渲染到一个QPixmap上，可以选择性地改变其填充颜色。
    这是在Qt中处理图标的专业方法。

    :param path: SVG文件的路径。
    :param size: 目标渲染尺寸。
    :param fill_color: (可选) 用于覆盖SVG填充色的颜色。
    :return: 渲染好的QPixmap。
    """
    # 1. 创建一个SVG渲染器
    renderer = QSvgRenderer(path)
    if not renderer.isValid():
        print(f"Error: Invalid SVG file at {path}")
        return QPixmap() # 返回一个空的Pixmap

    # 2. 创建一个空的、透明的画布 (QPixmap)
    pixmap = QPixmap(size)
    pixmap.fill(QColor("transparent")) # 保证背景透明

    # 3. 创建一个画家，让他在这张画布上作画
    painter = QPainter(pixmap)
    
    # 4. (可选，但极其强大) 如果提供了填充色，则进行颜色覆盖
    if fill_color:
        # 创建一个与画布等大的、填充了目标颜色的图层
        color_layer = QPixmap(size)
        color_layer.fill(fill_color)
        
        # 设置混合模式：只在SVG图形的“内部”进行着色
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.drawPixmap(0, 0, color_layer)

        # 恢复正常的混合模式，以便绘制SVG本身
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)

    # 5. 指示渲染器，将SVG内容画到画布上
    renderer.render(painter)
    
    # 6. 结束绘画
    painter.end()

    return pixmap


def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    一个递归函数，将一个嵌套字典“智能地”扁平化。
    例如：{'a': {'b': 1}} 会变成 {'a.b': 1}
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)

def smart_formatter(data: dict,text: str) -> str:
    placeholder_pattern = re.compile(r'\{([^{}]+)\}')
    def replacer(match):
        key = match.group(1)
        value = data.get(key, match.group(0))
        
        return str(value)
    
    return placeholder_pattern.sub(replacer, text)

def resource_path(relative_path):
        """ 获取资源的绝对路径，无论是开发环境还是打包后。 """
        try:
            # PyInstaller 创建一个临时文件夹，并通过 _MEIPASS 存放在 sys 中
            base_path = sys._MEIPASS
        except Exception:
            # 在开发环境中，_MEIPASS 不存在，所以我们用文件的绝对路径
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

LOG_FILE_PATH = "ti_debug_log.txt"
    
with open(LOG_FILE_PATH, "w") as f:
    f.write("--- Log Start ---\n")

def log_message(message):
    """将一条带有时间戳的消息写入日志文件。"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
