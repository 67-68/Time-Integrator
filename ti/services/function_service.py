from ti.model.plugin.function_contributions import FunctionContribution


class FunctionService:
    def __init__(self):
        self._functions = {}
    
    def regist_function(self,contribution: FunctionContribution):
        key = contribution.func_id
        func = contribution.func
        self._functions[key] = func
        
        print(f"[FUNC]successfully regist function {key}")
        
    def get_function(self,function_id) -> callable:
        return self._functions[function_id]
        
    
    