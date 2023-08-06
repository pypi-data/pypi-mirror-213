import dataclasses
import pprint


@dataclasses.dataclass
class NeonObject:

    def __init__(self, data: dict, obj_type: str = None) -> None:
        '''

        @param data: A dictionary of data representing an API return object
        @param obj_type: The type of the object to be stored.

        Some create functions return a large object with the primary object embedded as a field.
        The paginate functions just returned the embedded object. To allow the same init to be used for
        both types of returns we do some checking for the return type of the dict.
        '''
        self._type = obj_type
        self._create_data = None
        self._data = None
        if obj_type is None:
            self._data = None
        elif self._type in data:
            self._data = data[self._type]
            self._create_data = data
        else:
            self._data = data

    @property
    def is_created(self):
        return self._create_data is not None

    @property
    def created_data(self):
        return self._create_data

    def __getattr__(self, name):

        if name in self._data:
            return self._data[name]
        else:
            raise KeyError(f"'{name}' not found in {self._data}")

    @property
    def obj_data(self):
        return self._data

    @property
    def obj_type(self):
        return self._type

    def __str__(self) -> str:
        return pprint.pformat(self._data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data={self._data})"


class NeonOperation(NeonObject):

    def __init__(self, data: dict) -> None:
        self._type = "operation"
        super().__init__(data=data, obj_type=self._type)

class NeonProject(NeonObject):

    def __init__(self, data:dict) -> None:
        self._type = "project"
        super().__init__(data=data, obj_type=self._type)


class NeonBranch(NeonObject):

    def __init__(self, data: dict) -> None:
        self._type = "branch"
        super().__init__(data=data, obj_type=self._type)




class NeonEndPoint(NeonObject):
    def __init__(self, data: dict) -> None:
        self._type = "endpoint"
        super().__init__(data=data, obj_type=self._type)

