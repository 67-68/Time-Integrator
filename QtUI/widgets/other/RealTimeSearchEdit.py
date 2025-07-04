""" 数据往下，事件往上,任何尝试修改其自己的行为，指令都必须来源于上面 """
from PyQt6.QtWidgets import QLineEdit,QCompleter,QAbstractItemView
from PyQt6.QtCore import QStringListModel,Qt,QTimer

from Core.Definitions import UserActionType
from PyQt6.QtCore import QModelIndex

class RealTimeSearchEdit(QLineEdit):
    def __init__(self,wordBank = None,parent = None):
        super().__init__(parent)
        
    def initialization(self,wordBank):
        #  --- 添加词库 ---
        self.wordBank = wordBank
        self.model = QStringListModel(wordBank)
        
        #  --- 添加completer ---
        self.dropdown = QCompleter(self.model,self)
        self.dropdown.setFilterMode(Qt.MatchFlag.MatchContains)
        self.dropdown.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.dropdown.setWidget(self)       # 改为手动触发，禁用自动前缀
        
        #  --- 快捷赋值 ---
        self.view = self.dropdown.popup()
    
    """  ------ dropdown功能 ------ """
    #INPUT action String; UPDATE completer, use it to filter wordbank
    def set_dropdown_prefix(self, key):
        """Update prefix manually and keep popup visible."""
        if not key:                               # 空串就收起
            self.dropdown.popup().hide()
            return

        self.dropdown.setCompletionPrefix(key)    # 手动设前缀
        if self.dropdown.completionCount():       # 有匹配才弹
            self.dropdown.complete()
        else:
            self.dropdown.popup().hide()
            
    #UNIVERSAL; INPUT tk dropdown and int index; UPDATE dropdown
    def switchDropdown(self,index):
            self.view.setCurrentIndex(self.model.index(index,0))
            self.view.scrollTo(self.model.index(index, 0), QAbstractItemView.ScrollHint.EnsureVisible)
            self.view.clearSelection()
            self.view.setCurrentIndex(QModelIndex())
    
    #SPECIFIC; INPUT actionState; UPDATE dropdown
    def updateDropdown(self, actionState):
        #  --- 获取当前被选中项 ---
        selected = self.dropdown.currentIndex()
        
        #  --- 判断是否已经被选中 ---
        if selected.isValid(): #这里选了判断是否选中，所以上面不用判定了
            index = selected.row()
        else:
            index = -1
    
        if actionState == UserActionType.ARROW_UP:
            new_index = max(index - 1, 0)

        elif actionState == UserActionType.ARROW_DOWN:
            size = self.dropdown.size()
            if index + 1 >= size:
                new_index = 0 
            else:
                new_index = index + 1
        else:
            return

        self.switchDropdown(new_index)
        
    """ ------ API函数 ------ """
    def getDropdownVisibility(self):
        return self.dropdown.popup().isVisible()
    
    def getDropdownSelection(self):
        return self.dropdown.popup().currentIndex()
    
    def getDropdownVal(self,row):
        if self.dropdown is None:
            return ""
        elif self.dropdown.model() is None:
            return ""
        else:
            return self.dropdown.model().index(row,0).data()
        
    def getDropdownKey(self):
        return self.dropdown.completionPrefix()