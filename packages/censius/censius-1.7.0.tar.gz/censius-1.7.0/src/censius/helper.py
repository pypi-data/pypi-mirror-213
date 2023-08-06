from jsonschema import validate, exceptions
from typing import Any, Tuple


def validate_input(kwargs, define_schema) -> Tuple[bool, dict]:
    try:
        validate(instance=kwargs, schema=define_schema)
    except exceptions.ValidationError as err:
        status_code = 400
        err.message = err.schema.get("errorMessage", err.message)
        return True, {"status": "error", "details": err.message}
    return False, None
