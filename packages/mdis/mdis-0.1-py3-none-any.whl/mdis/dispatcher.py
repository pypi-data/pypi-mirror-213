from . import core as _core


class DispatcherMeta(type):
    @classmethod
    def dispatch(metacls, typeid=object):
        module = typeid.__module__
        qualname = typeid.__qualname__
        if module == "builtins":
            return qualname
        return f"{module}.{qualname}".replace(".", "_")

    def __new__(metacls, name, bases, ns):
        hooks = {}

        for (key, value) in tuple(ns.items()):
            if isinstance(value, _core.CallHook):
                hook = ns.pop(key)
                for typeid in hook.typeids:
                    site = metacls.dispatch(typeid)
                    hooks[typeid] = (hook, site)

        for (typeid, (hook, site)) in tuple(hooks.items()):
            ns[site] = hook

        return super().__new__(metacls, name, bases, ns)


class Dispatcher(metaclass=DispatcherMeta):
    def __call__(self, instance):
        nil = object()
        for typeid in instance.__class__.__mro__:
            site = self.__class__.dispatch(typeid)
            call = getattr(self, site, nil)
            if call is not nil:
                return call(self, instance)
        return getattr(self, self.__class__.dispatch())
