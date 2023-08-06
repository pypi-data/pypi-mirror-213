from datetime import datetime
from typing import Dict
from warnings import warn

from ecmind_blue_client import Client, Job
from ecmind_blue_client.const import MainTypeId
from XmlElement import XmlElement

from ecmind_blue_client_objdef import (Cabinet, Field, FieldTypes, Object,
                                       TableColumn, TableField)

from .addons import Addons, ListAddon, ListAddonRow


class ObjectDefinition():
    def __init__(self, obj_def_xml:str):
        xml_elem = XmlElement.from_string(obj_def_xml)
        xml_elem.find('languages').find('language').flag_as_list = True
        for cab in xml_elem.findall('cabinet'):
            cab.flag_as_list = True
            for obj in cab.findall("object"):
                obj.flag_as_list = True
        self.raw = xml_elem.to_dict()

        self.created = datetime.strptime(xml_elem.attributes['created'], '%Y-%m-%dT%H:%M:%S')
        self.languages = { l['@name']: l['@lang_id'] for l in self.raw['languages']['language'] }
        language_by_id = { l['@lang_id']: l['@name'] for l in self.raw['languages']['language'] }

        self.cabinets:Dict[str, Cabinet] = {}
        self.registers:Dict[str, Object] = {}
        self.documents:Dict[str, Object] = {}

        for raw_cabinet in self.raw['cabinet']:
            if isinstance(raw_cabinet['object'], list):
                raw_objects = raw_cabinet['object']
            else:
                raw_objects = [ raw_cabinet['object'] ]
            
            def __parse_fields__(raw_list:dict, page_control:Field=None, page:str=None) -> dict:
                fields = {}
                if not isinstance(raw_list, list):
                    raw_list = [ raw_list ]

                for raw_field in raw_list:
                    raw_names = raw_field['names']['name']
                    if not isinstance(raw_names, list):
                        raw_names = [ raw_names ]


                    internal_name = raw_field['@internal']
                    name = raw_field['@name']
                    names = { language_by_id[n['@lang_id']]: n['#'] for n in raw_names }
                    db_field = ['@fieldname']
                    guid = raw_field['@os_guid']
                    tab_order = raw_field['@taborder']
                    length = raw_field['flags']['@input_length'] if '@input_length' in raw_field['flags'] else 0

                    try:
                        field_type = FieldTypes(str(raw_field['flags']['@dt']))
                    except Exception as _:
                        field_type = None
                        warn(f'Datatype "{str(raw_field["flags"]["@dt"])}" for field {raw_field["@internal"]} is unknown.')

                    addons = Addons()

                    # List or Addons
                    if "list" in raw_field: 
                        addon_data = raw_field['list']

                        # List / Tree Addon
                        if 'ADDON32' not in raw_field['list']:
                            multiselection = addon_data['@multiselection'] == 1
                            order = addon_data['@order']
                            keyselcol =  addon_data['@keyselcol'] if '@keyselcol' in addon_data else 0
                            sortcol = addon_data['@sortcol'] if '@sortcol' in addon_data else 0
                            rawdata = addon_data['rawdata']
                            
                            # List
                            if 'row' in addon_data:
                                icon_index = 0
                                icons = []
                                while f'ICON{icon_index}' in addon_data:
                                    icons.append(addon_data[f'ICON{icon_index}'])
                                    icon_index += 1

                                rows = []
                                row_index = 0
                                for row in addon_data['row']:
                                    rows.append(ListAddonRow(row, icons, row_index))

                                addons.list = ListAddon(rows, multiselection, order, keyselcol, sortcol, rawdata)


                    if field_type == FieldTypes.TABLE:
                        columns:Dict[str, TableColumn] = {}
                        if 'listctrl' in raw_field:
                            for raw_column in raw_field['listctrl'] if isinstance(raw_field['listctrl'], list) else [ raw_field['listctrl'] ]:
                                raw_col_names = raw_column['names']['name'] if isinstance(raw_column['names']['name'], list) else [ raw_column['names']['name'] ]
                                columns[raw_column['@internal']] = TableColumn(
                                    internal_name=raw_column['@internal'],
                                    name=raw_column['@name'],
                                    names={ language_by_id[n['@lang_id']]: n['#'] for n in raw_col_names },
                                    db_field=raw_column['@fieldname'],
                                    id=raw_column['@id'],
                                    type=FieldTypes(str(raw_column['@type'])),
                                    length=raw_column['@length'],
                                    guid=raw_column['@os_guid']
                                )
                        else:
                            warn(f'Table "{str(internal_name)}" (GUID {guid}) has no columns.')

                        field = TableField(internal_name, name, names, db_field, field_type, length, guid, tab_order, page_control, page, columns)
                    else:
                        field = Field(internal_name, name, names, db_field, field_type, length, guid, tab_order, page_control, page, addons)

                    
                    fields[raw_field['@internal']] = field

                    if 'page' in raw_field:
                        if isinstance(raw_field['page'], list):
                            raw_pages = raw_field['page']
                        else:
                            raw_pages = [ raw_field['page'] ]
                        for raw_page in raw_pages:
                            if '@internal' in raw_page:
                                page = raw_page['@internal']
                            else:
                                page = raw_page['@page_id']
                                warn(f'Page "{raw_page["@page_id"]}" has no internal name.')
                            if raw_page['fields'] != None:                                    
                                fields.update(
                                    __parse_fields__(
                                        raw_page['fields']['field'],
                                        page_control=field, 
                                        page=page
                                    )
                                )
                            else:
                                warn(f'Page "{page}" of page control "{internal_name}" has no elements.')
                    
                return(fields)

            cabinet_registers:Dict[str, Object] = {}
            cabinet_document:Dict[str, Object] = {}
            for raw_child in raw_objects:
                
                if raw_child['@maintype'] == MainTypeId.FOLDER.value:
                    cabinet_fields = __parse_fields__(raw_child['fields']['field'])  
                else:
                    child = Object(
                        type_id= raw_child['@maintype']* 2**16 + raw_child['@cotype'],
                        internal_name=raw_child['@internal'],
                        name=raw_child['@name'],
                        table_name=raw_child['@tablename'],
                        fields = __parse_fields__(raw_child['fields']['field'])  
                    )

                    if raw_child['@maintype'] == MainTypeId.REGISTER.value:
                        self.registers[raw_child['@internal']] = child
                        cabinet_registers[raw_child['@internal']] = child
                    else:
                        self.documents[raw_child['@internal']] = child
                        cabinet_document[raw_child['@internal']] = child
            cabinet = Cabinet(
                type_id=raw_cabinet['@cotype'],
                internal_name=raw_cabinet['@internal'],
                name=raw_cabinet['@name'],
                table_name=[o for o in raw_cabinet['object'] if o["@maintype"] == 0][0]['@tablename'],
                fields=cabinet_fields,
                registers=cabinet_registers,
                documents=cabinet_document
            )

            self.cabinets[cabinet.internal_name] = cabinet

    def __repr__(self) -> str:
        return f'Cabinets: {len(self.cabinets)}, Registers: {len(self.registers)}, Documents: {len(self.documents)}, Languages: {len(self.languages)}'


def load_object_definition(client:Client) -> ObjectDefinition:
    get_objdef_result = client.execute(Job(
        'dms.GetObjDef',
        Flags=1+4096
    ))
    if not get_objdef_result.return_code == 0:
        raise RuntimeError(get_objdef_result.error_message)
    
    object_definition = ObjectDefinition(get_objdef_result.values['sRet'])
    return object_definition