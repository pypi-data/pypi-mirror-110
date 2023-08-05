from enum import Enum
from typing import Any, List, Optional

from ..typing.dataclass import dataclass


class Type(str, Enum):
    int = "int"
    bigint = "bigint"
    enum = "enum"

    str = "str"
    uuid = "uuid"
    email = "email"
    url = "url"

    float = "float"

    date = "date"
    datetime = "datetime"
    auto_now = "now"
    auto_now_add = "auto_now_add"

    timedelta = "timedelta"

    json = "json"
    binary = "binary"

    foreign = "foreign"
    m2m = "m2m"


@dataclass
class Field:
    name: str
    title: str
    fieldType: Type
    length: int = 0

    description: str = ""

    default: Any = None
    index: bool = False
    required: bool = False
    unique: bool = False

    to: Optional[str] = None

    allow_update: bool = True


@dataclass
class Scheme:
    name: str

    fields: List[Field]
    pk: str = "id"
