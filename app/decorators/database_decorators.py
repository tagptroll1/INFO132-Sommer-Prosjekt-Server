from functools import wraps

from bson.objectid import ObjectId


def convert_id(func):
    """
    Converts string & int ids to bson.ObjectId.

    Decorator for database function which converts a given
    integer or string to a bson.ObjectId object before passing
    it to the function.  This decorator also takes the `id` parameter
    if provided and converts it to `_id` for mongodb to use.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("_id"):
            if isinstance(kwargs["_id"], list):
                kwargs["_id"] = [ObjectId(id_) for id_ in kwargs["_id"]]
            else:
                kwargs["_id"] = ObjectId(kwargs["_id"])
        elif kwargs.get("id"):
            if isinstance(kwargs["id"], list):
                kwargs["_id"] = [ObjectId(id_) for id_ in kwargs["id"]]
            else:
                kwargs["_id"] = ObjectId(kwargs["id"])
            del kwargs["id"]

        return func(*args, **kwargs)
    return wrapper
