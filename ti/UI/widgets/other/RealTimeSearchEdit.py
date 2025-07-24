""" 数据往下，事件往上,任何尝试修改其自己的行为，指令都必须来源于上面 """
from PyQt6.QtWidgets import QLineEdit,QCompleter,QAbstractItemView
from PyQt6.QtCore import QStringListModel,Qt,QSignalBlocker

from Core.Definitions import UserActionType
from PyQt6.QtCore import QModelIndex

class RealTimeSearchEdit(QLineEdit):
    def __init__(self,wordBank = None,parent = None):
        super().__init__(parent)
        
        #  --- 初始化映射表 ---
        self.dropdownActions = {
            Qt.Key.Key_Up:self._on_key_down_pressed,
            Qt.Key.Key_Down:self._on_key_up_pressed,
            Qt.Key.Key_Return:self._on_dropdown_confirm
        }

        
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
    def setPrefix(self,key):
        self.dropdown.setCompletionPrefix(key)
        self.dropdown.complete()
        
    def keyPressEvent(self, a0):
        if self.dropdown.popup().isVisible():
            key = a0.key()
            if key in self.dropdownActions:
                #手动补一个判定
                if key is not Qt.Key.Key_Return or self.dropdown.popup().currentIndex():
                    self.dropdownActions[key]()
                    return "break"
        
        return super().keyPressEvent(a0)

    #确认，最终修改文本框
    def _on_dropdown_confirm(self):
        cur_index = self.dropdown.popup().currentIndex()
        if not cur_index.isValid():        # 若没有选中项则直接返回
            return
        row = cur_index.row()
        selectedVal = self.getDropdownVal(row)
        key = self.dropdown.completionPrefix()
        text = self.text()
        
        #这里如果没有key(空)，那么会出问题
        if key:
            newText = text.replace(key,selectedVal) 
        else:
            newText = text + selectedVal
        
        self.setText(newText)   #这里好像不能signal blocker
        self.dropdown.popup().hide()  #手动hide popup
    
    #UNIVERSAL; INPUT tk dropdown and int index; UPDATE dropdown
    def switchDropdown(self,index):
            self.view.setCurrentIndex(self.model.index(index,0))
            self.view.scrollTo(self.model.index(index, 0), QAbstractItemView.ScrollHint.EnsureVisible)
            self.view.clearSelection()
            self.view.setCurrentIndex(QModelIndex())
    
    #SPECIFIC; INPUT actionState; UPDATE dropdown
    def _on_key_down_pressed(self):
        #  --- 获取当前被选中项 ---
        selected = self.dropdown.currentIndex()
        
        #  --- 判断是否已经被选中 ---
        if selected.isValid(): #这里选了判断是否选中，所以上面不用判定了
            index = selected.row()
        else:
            index = -1

        size = self.dropdown.size()
        if index + 1 >= size:
            new_index = 0 
        else:
            new_index = index + 1
        
        self.switchDropdown(new_index)
        
        
    def _on_key_up_pressed(self):
        #  --- 获取当前被选中项 ---
        selected = self.dropdown.currentIndex()
        
        #  --- 判断是否已经被选中 ---
        if selected.isValid(): #这里选了判断是否选中，所以上面不用判定了
            index = selected.row()
        else:
            index = -1
        
        new_index = max(index - 1, 0)
        self.switchDropdown(new_index)
        
        
    """ ------ API函数 ------ """
    def getDropdownVal(self, row):
        """
        Return the string shown in the *filtered* popup at `row`.
        Must index via the popup’s model rather than the source model;
        otherwise the value will be wrong when the list is filtered.
        """
        if self.dropdown is None:
            return ""
        pop_model = self.dropdown.popup().model()
        if pop_model is None:
            return ""
        return pop_model.index(row, 0).data()
        