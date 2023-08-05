import functools
import json
from datetime import date, datetime
from typing import Any


def json_serilize(o: Any):
    if isinstance(o, datetime) or isinstance(o, date):
        return o.isoformat()
    raise TypeError(f"Type {type(o)} not serializable")


def json_deserilize(o: Any):
    for k, v in o.items():
        if isinstance(v, str) and v.find("T") == 10:
            try:
                o[k] = datetime.fromisoformat(v)
            except ValueError:
                pass
    return o


json_dumps = functools.partial(
    json.dumps, separators=(",", ":"), default=json_serilize
)
json_loads = functools.partial(json.loads, object_hook=json_deserilize)
