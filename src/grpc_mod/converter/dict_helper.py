from typing import Any, Dict
from api.undefined import UNDEFINED


def drop_undefined(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively drops fields with value UNDEFINED and as false interpreted values from a dictionary."""
    if not isinstance(data, dict):
        return data
    return {
        key: drop_undefined(value)
        for key, value in data.items()
        if value is not UNDEFINED and value not in (None, '', [], {}, ())
    }

def drop_except_keys(data: Dict[str, Any], keys_to_keep: set) -> Dict[str, Any]:
    """Drops all fields except those specified in keys_to_keep."""
    if not isinstance(data, dict):
        return data
    return {
        key: drop_except_keys(value, keys_to_keep)
        for key, value in data.items()
        if key in keys_to_keep
    }