class TypeidHook(object):
    def __init__(self, *typeids, wrapper=lambda call: call):
        for typeid in typeids:
            if not isinstance(typeid, type):
                raise ValueError(typeid)
        self.__typeids = typeids
        self.__wrapper = wrapper
        return super().__init__()

    def __iter__(self):
        yield from self.__typeids

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__typeids})"

    def __call__(self, call):
        if not callable(call):
            raise ValueError(call)
        return CallHook(typeids=self, call=call, wrapper=self.__wrapper)


class CallHook(object):
    def __init__(self, typeids, call, wrapper=lambda call: call):
        if not isinstance(typeids, TypeidHook):
            raise ValueError(typeids)
        if not callable(call):
            raise ValueError(call)
        self.__typeids = typeids
        self.__call = wrapper(call)
        return super().__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}(call={self.call!r}, typeids={self.typeids!r})"

    @property
    def typeids(self):
        return self.__typeids

    @property
    def call(self):
        return self.__call

    def __call__(self, visitor, instance):
        return self.__call(visitor, instance)


def hook(*typeids):
    return TypeidHook(*typeids)
