from typing import Any

from tortoise import fields

from .serilize import json_dumps, json_loads


class JSONField(fields.JSONField):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(encoder=json_dumps, decoder=json_loads, **kwargs)
