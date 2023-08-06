class ListAddonRow:
    """
    A class to represent a list row entry.

    Attributes
    ----------
    index : int
        Index if the row in the list
    icon_id : int
        icon id if defined. Else 0
    value : string
        entry value
    label : string
        translated lable of the entry if defined. Else identical to value
    """

    index: int
    icon_id: int
    value: str
    label: str

    def __init__(self, raw_row, icons, index):
        # Set index if information exists, else use default order
        self.index = raw_row["@index"] if "@index" in raw_row else index

        # set icon id if defined, else 0
        if self.index < len(icons):
            self.icon_id = icons[self.index]
        else:
            self.icon_id = 0

        # set value and label identical if value is a string
        if isinstance(raw_row, str):
            self.value = raw_row
            self.label = raw_row
        else:
            self.value = raw_row["@value"] if "@value" in raw_row else raw_row["#"]
            self.label = raw_row["#"]


class ListAddon:
    """
    A class to represent field list addon

    Attributes
    ----------
    rows : list[ListAddonRow]
        list entries
    multiselection : boolean
        defines if multiselection is allowed
    order : int
        Unknown
    keyselcol : int
        Unknown
    sortcol : int
        Unknown
    rawdata : string
        Raw Addon informations
    """

    rows: list[ListAddonRow]
    multiselection: bool
    order: int
    keyselcol: int
    sortcol: int
    rawdata: str

    def __init__(
        self,
        rows: list[ListAddonRow],
        multiselection: bool = False,
        order: int = 0,
        keyselcol: int = 0,
        sortcol: int = 0,
        rawdata: str = "",
    ):
        self.multiselection = multiselection
        self.order = order
        self.keyselcol = keyselcol
        self.sortcol = sortcol
        self.rawdata = rawdata
        self.rows = rows


class Addons:
    """
    A class to represent the possible field addons

    Attributes
    ----------
    list_addon : ListAddon | None
        list addon or None if the field has no list addon
    """

    def __init__(self, list_addon: ListAddon = None):
        self.list = list_addon
