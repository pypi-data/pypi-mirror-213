from typing import Dict

from ecmind_blue_client_objdef import FieldTypes
from .addons import Addons

class Field():
    def __init__(
        self, 
        internal_name:str, 
        name:str,
        names:Dict[str, str],
        db_field:int, 
        type:FieldTypes,
        length:int,
        guid:str,
        tab_order:int,
        page_control:str=None,
        page:str=None,
        addons: Addons=None
    ):
        self.internal_name = internal_name
        self.name = name
        self.names = names
        self.db_field = db_field
        self.type = type
        self.length = length
        self.guid = guid
        self.tab_order = tab_order
        self.page_control = page_control,
        self.page = page
        self.addons = addons

    def __repr__(self) -> str:
        return f'{self.internal_name} ({self.db_field}) "{self.name}"'