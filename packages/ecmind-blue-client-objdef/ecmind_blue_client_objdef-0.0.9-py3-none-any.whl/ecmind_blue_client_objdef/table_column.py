from typing import Dict
from ecmind_blue_client_objdef import FieldTypes

class TableColumn():
    def __init__(
        self, 
        internal_name:str, 
        name:str,
        names:Dict[str, str],
        db_field:str, 
        id:int,
        type:FieldTypes,
        length:int,
        guid:str
    ):
        self.internal_name = internal_name
        self.name = name
        self.names = names
        self.db_field = db_field
        self.id = id
        self.type = type
        self.length = length
        self.guid = guid

    def __repr__(self) -> str:
        return f'{self.id}: {self.internal_name} ({self.db_field}) "{self.name}"'