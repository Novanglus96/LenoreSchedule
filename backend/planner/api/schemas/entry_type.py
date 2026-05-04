from ninja import Schema


class EntryTypeIn(Schema):
    name: str
    code: str


class EntryTypeOut(Schema):
    id: int
    name: str
    code: str
