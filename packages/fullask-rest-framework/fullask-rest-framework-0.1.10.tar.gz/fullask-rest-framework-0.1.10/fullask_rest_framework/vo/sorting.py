class SortingRequest:
    def __init__(self, *args):
        """
        SortingRequest({"uuid":"asc"})
        """
        for arg in args:
            for field, search_word in arg.items():
                setattr(self, field, search_word)

    def __repr__(self):
        attrs = [f"{attr}={value!r}" for attr, value in vars(self).items()]
        return f"{self.__class__.__name__}({', '.join(attrs)})"
