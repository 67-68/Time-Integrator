from ti.core.Interfaces.jsonRepositoryInterface import JsonRepositoryInterface
from ti.dataAccess.dataAccess import getData, saveData
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
        self.contracts = self.load()
        super().__init__()

    @property
    def filePath(self):
        return "ti/features/intervention/model/contracts.json"
    
    def save(
        self,
        data: dict[INV_Contract]
    ):
        self.contracts = data
        
        raw_data = {
            contract_id: contract.to_dict()
            for contract_id, contract in self.contracts
        }
        
        saveData(raw_data,self.filePath)
        return super().save()
    
    def load(self) -> dict[INV_Contract]:
        rawData = getData(self.filePath)
        for contract_id, contract_dict in rawData.items():
            self.contracts[contract_id] = INV_Contract.from_dict(contract_dict)
        
        return self.contracts
    
    def add_contract(self,contract:INV_Contract):
        self.contracts[contract.contract_uuid] = contract
        print(f"添加完成contract{contract.contract_uuid}")
        
    def get_by_id(self, contract_id: str) -> INV_Contract | None:
        # 深拷贝一份返回，防止外部代码意外修改了缓存中的“真理”
        import copy
        print("尝试获取contract数据...")
        contract = self.contracts.get(contract_id)
        return copy.deepcopy(contract) if contract else print("contract数据中没有东西")
    