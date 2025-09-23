class SessionCache:
    def __init__(self):
        """_summary_
        临时上下文服务
        """
        self._cache = {}
    
    def store(self,key,data):
        """_summary_
        存储输入的数据
        cache["key"] = data
        Args:
            key (_type_): _description_
            data (_type_): _description_
        """
        self._cache[key] = data
    
    def read(self,key):
        """_summary_
        阅读数据
        Args:
            key (_type_): _description_
        """
        return self._cache.get(key)
    
    def reset(self):
        """_summary_
        清除所有数据
        """
        self._cache = {}