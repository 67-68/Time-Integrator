from dataclasses import dataclass

from ti.model.synthesizer_data import SynthesizerRegistry


class Synthesizer:
    """
    这个类负责管理多个东西之间的互通
    """
    def __init__(self):
        self.syn = {}
        
    def regist_synthesize(
        self,
        data: SynthesizerRegistry
    ):
        syn_id = data.syn_id
        func = data.func
        if syn_id in self.syn:
            print(f"first registry {syn_id}")
            self.syn[syn_id] = []
        else:
            print(f"regist_{syn_id}")
        
        self.syn[syn_id].append(func)
        
    def publish_data(self,syn_id,data):
        print(f"publish synthesize in {syn_id}")
        for func in self.syn[syn_id]:
            func(data)
        


    
    