class Data:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                if isinstance(value, dict):
                    value = Data(value)
                setattr(self, key, value)

    def __len__(self):
        return len(self.__dict__.keys())


class Event:
    def __init__(self, e_type: str, data_dict=None):
        self.type = e_type
        self.data = Data(data_dict)

    def has_data(self):
        return len(self.data) > 0
