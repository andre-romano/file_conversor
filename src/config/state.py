# src\config\state.py


class State:

    __instance = None

    @staticmethod
    def get_instance():
        if not State.__instance:
            State.__instance = State()
        return State.__instance

    def __init__(self) -> None:
        super().__init__()

        # Define state dictionary
        self.__data = {
            "verbose": False,
        }

    def __repr__(self) -> str:
        return repr(self.__data)

    def __str__(self) -> str:
        return str(self.__data)

    def __getitem__(self, key):
        return self.__data[key]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __contains__(self, key):
        return key in self.__data

    def __len__(self):
        return len(self.__data)

    def clear(self):
        self.__data.clear()

    def update(self, new: dict):
        self.__data.update(new)
