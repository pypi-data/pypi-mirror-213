from typing import Dict, List
from ecmind_blue_client_objdef import Object, Field

class Cabinet(Object):
    def __init__(self, type_id:int, internal_name:str, name:str, table_name:str, fields:List[Field]=None, registers:Dict[str, Object]={}, documents:Dict[str, Object]={}):
        super().__init__(type_id, internal_name, name, table_name, fields)
        self.registers = registers
        self.documents = documents