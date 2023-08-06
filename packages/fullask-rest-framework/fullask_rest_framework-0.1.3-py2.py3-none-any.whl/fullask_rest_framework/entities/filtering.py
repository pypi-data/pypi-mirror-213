class FilteringRequest:
    def __init__(self, **kwargs):
        super().__init__()
        for field, search_word in kwargs.items():
            setattr(self, field, search_word)

    def __repr__(self):
        attrs = [f"{attr}={value!r}" for attr, value in vars(self).items()]
        return f"{self.__class__.__name__}({', '.join(attrs)})"
