from PyQt6.QtWidgets import QLineEdit,QCompleter,QAbstractItemView
from PyQt6.QtCore import QStringListModel,Qt

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
        self.setCompleter(self.dropdown)
        
        #  --- 快捷赋值 ---
        self.view = self.dropdown.popup()

    #INPUT action String; UPDATE completer, use it to filter wordbank
    def showFilter(self, actionStr):
        text = actionStr if not None else ""
        
        if not text: 
            self.model.setStringList(self.wordBank)
        else:
            filterList = []
            for word in self.wordBank:
                if text.lower() in word.lower():
                    filterList.append(word)
            self.model.setStringList(filterList)

            if self.completer() is None:
                self.setCompleter(self.dropdown)
            self.dropdown.setCompletionPrefix("")      # 清空 prefix 避免Qt再过滤
            self.dropdown.complete()                   # ⬅ always call complete
        
        
    def hideDropdown(self):
        self.dropdown.popup().hide()
    
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
        if selected.isValid():
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