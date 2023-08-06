from . import core as _core
from . import dispatcher as _dispatcher


class WalkerMeta(_dispatcher.DispatcherMeta):
    @classmethod
    def dispatch(metacls, typeid):
        return ("walk_" + super().dispatch(typeid))


class Walker(_dispatcher.Dispatcher, metaclass=WalkerMeta):
    @_core.hook(tuple, list, set, frozenset)
    def sequence(self, instance):
        for item in instance:
            yield item
            yield from self(item)

    @_core.hook(dict)
    def mapping(self, instance):
        for (key, value) in instance.items():
            yield (key, value)
            yield from self((key, value))

    @_core.hook(object)
    def object(self, instance):
        yield from ()
