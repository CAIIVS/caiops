def has_method(obj: object, method_name: str):
    return method_name in obj.__class__.__dict__
