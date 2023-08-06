import contextlib as _contextlib

from . import core as _core
from . import dispatcher as _dispatcher


class VisitorMeta(_dispatcher.DispatcherMeta):
    @classmethod
    def dispatch(metacls, typeid):
        return ("visit_" + super().dispatch(typeid))


class Visitor(_dispatcher.Dispatcher, metaclass=VisitorMeta):
    @_core.hook(object)
    def object(self, instance):
        yield instance
