from uuid import UUID
from ti.core.Interfaces.json_repository_interface import JsonRepositoryInterface
from ti.services.dataAccess.dataAccess import getData, saveData
from ti.features.intervention.model.model import INV_Contract


class INV_ContractRepository(JsonRepositoryInterface):
    def __init__(self):
        """_summary_
        存储contract本身，而不是recipe
        存储动态的contract实例
        在软件关闭后仍然可以运行
        加载所有的文件出来
        """
        self.contracts = {}
        self.contracts = self.load() #错误在这里！是不是初始化的时候为空导致错误？
        super().__init__()

    @property
    def filePath(self):
        return "features/intervention/model/contracts.json"
    
    # in INV_ContractRepository.save

    def save(
        self,
        data: dict[UUID, INV_Contract] # 建议把key的类型也写上，更清晰
    ):
        """
        一次性保存所有数据
        """
        self.contracts = data
        
        # 明确地告诉Python，我们要遍历“键值对 (items)”
        raw_data = {
            # 注意！这里需要把UUID对象转换为字符串，因为JSON不支持UUID作为key
            str(contract_id): contract.to_dict() 
            for contract_id, contract in self.contracts.items() # <--- 使用 .items()
        }
        
        saveData(raw_data, self.filePath)
        print(f"保存了数据{raw_data}")
        
        # 你这里调用了super().save()，但你的基类JsonRepositoryInterface
        # 可能没有save方法，如果报错可以先注释掉
        # return super().save() 
    
    def load(self) -> dict[INV_Contract]:
        rawData = getData(self.filePath)
        for contract_uuid, contract_dict in rawData.items():
            if contract_dict:
                self.contracts[contract_uuid] = INV_Contract.from_dict(contract_dict) # 这里为什么保存了一个空的{}?
        
        return self.contracts
    
    def add_contract(self,contract:INV_Contract):
        """
        如果uuid重合，会覆盖
        自动保存

        Args:
            contract (INV_Contract): _description_
        """
        if contract.contract_uuid in self.contracts:
            print(f"覆盖contract{contract.contract_category_id}")
    
        self.contracts[contract.contract_uuid] = contract
        print(f"添加完成contract{contract.contract_uuid}")
        self.save(self.contracts)
            
    def get_by_id(self, contract_id: str) -> INV_Contract | None:
        # 深拷贝一份返回，防止外部代码意外修改了缓存中的“真理”
        import copy
        print("尝试获取contract数据...")
        contract = self.contracts.get(contract_id)
        return copy.deepcopy(contract) if contract else print("contract数据中没有东西")

    def get_by_view_id(self,view_id):
        for contract_uuid in self.contracts:
            if self.contracts[contract_uuid].view_recipe_id == view_id:
                return self.contracts[contract_uuid]
    
    def delete(self,contract_uuid):
        """
        负责从库中删除一个contract

        Args:
            contract_uuid (_type_): _description_
        """
        print(f"试图删除{contract_uuid},但是这个方法还没写")