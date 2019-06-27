from functools import wraps

from bson.objectid import ObjectId


def json_serialize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)

        def convert_ObjectId(item):
            for key, value in item.items():
                if isinstance(value, ObjectId):
                    item[key] = str(value)

        if return_value is None:
            return None

        if isinstance(return_value, list):
            for item in return_value:
                convert_ObjectId(item)
        elif isinstance(return_value, tuple):
            assert len(return_value) == 2  # Assert it's (data, status) tuple
            convert_ObjectId(return_value[0])
        else:
            convert_ObjectId(return_value)

        return return_value
    return wrapper
