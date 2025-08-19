from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str):
        self.path = path.split(".")

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        data = instance.payload
        try:
            for i in range(len(self.path)):
                data = data.get(self.path[i])
        except AttributeError:
            return None
        return data

    def __set__(self, instance, value):
        data = instance.payload
        for key in self.path:

            if key == self.path[-1]:
                data[key] = value
            else:
                data = data[key]
