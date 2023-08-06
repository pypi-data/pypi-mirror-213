from typing import Dict
from ecmind_blue_client_objdef import Field, FieldTypes, TableColumn

class TableField(Field):
    def __init__(
        self, 
        internal_name:str, 
        name:str,
        names:Dict[str, str],
        db_field:str, 
        type:FieldTypes,
        length:int,
        guid:str,
        tab_order:int,
        page_control:str=None,
        page:str=None,
        columns:Dict[str, TableColumn]={}
    ):
        super().__init__(internal_name, name, names, db_field, type, length, guid, tab_order, page_control, page)
        self.columns:Dict[str, TableColumn] = columns