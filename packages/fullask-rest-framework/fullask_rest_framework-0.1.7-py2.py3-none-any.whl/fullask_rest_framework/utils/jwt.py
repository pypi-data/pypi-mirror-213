from copy import deepcopy
from functools import wraps

from flask_jwt_extended import jwt_required as original_jwt_required


def jwt_required(*args, **kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            return original_jwt_required(*args, **kwargs)(func)(*f_args, **f_kwargs)

        wrapper._apidoc = deepcopy(getattr(func, "_apidoc", {}))
        wrapper._apidoc.setdefault("manual_doc", {})
        wrapper._apidoc["manual_doc"]["security"] = [{"Bearer Auth": []}]
        return wrapper

    return decorator
