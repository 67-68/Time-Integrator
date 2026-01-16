


from ti.view.page_view import PageView


class PageFactory:
    def __init__(self,bus):
        self.bus = bus
    
    def create_page(self,page_name,parent) -> PageView:
        return PageView(self.bus,page_name,parent=parent)