
from typing import Dict, List
from ecmind_blue_client_objdef import Field

class Object():
    def __init__(self, type_id:int, internal_name:str, name:str, table_name:str, fields:List[Field]=None):
        self.type_id = type_id
        self.internal_name = internal_name
        self.name = name
        self.table_name = table_name
        self.fields:Dict[str, Field] = fields

    def __repr__(self) -> str:
        return f'{self.internal_name} ({self.type_id}) "{self.name}"'