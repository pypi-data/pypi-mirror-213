# About this project

The mdis module allows to quickly extend the classes with the required functionality without modifications inside these classes.
This is done via double dispatch pattern: the dispatcher describes the required action based on the the argument type.
Use cases mainly include visitors and iterators, but are not limited to them.

# Dispatchers

The key concept of this module is dispatcher. A dispatcher object is a callable object; the exact call logic depends on the type of the argument.
The main class, `mdis.dispatcher.Dispatcher`, can register per-type hooks, which modify the call logic depending on the argument.
The hook is registered on a dispatcher class level as a method; attempts to call a dispatcher determine the relevant hooks based on argument type.

# Walkers

Sometimes objects of different types need to be traversed, but either lack `__iter__` method, or its semantics differs from what the users want.
For example, let's consider a nested collection, consisting of tuples, dicts and other types.
`dict.__iter__` method yields just keys, and the values have to be got via `__getitem__` calls.
Also, in order to support nested collections, users will have to write some recursive code with `isinstance` checks.
With `mdis.Walker`, users can just install the handlers for the types of interest, and change the iteration logic.
A walker is just a particular example of dispatcher, where the call yields some objects in a class-dependent manner.
The default `mdis.Walker` already incorporates the logic to walk over some builtin Python objects.
The example below shows how to override the way the dicts are traversed so that keys and values are swapped.

    import mdis.core
    import mdis.walker

    class CustomWalker(mdis.walker.Walker):
        @mdis.core.hook(dict)
        def walk_dict(self, instance):
            for (key, value) in instance.items():
                yield (value, key)
                yield from self((value, key))

    collection = {"a": 1, "b": 2}
    walker = CustomWalker()
    for item in walker(collection):
        print(item)

The following output is expected:

    (1, 'a')
    1
    a
    (2, 'b')
    2
    b

# Visitors

In `mdis`, a visitor is just another particular example of dispatcher.
Whenever the visitor is called, the call is dispatched based on type, and some per-class action is performed.
The primary scenario is to combine the visitor calls with context managers.
The example below shows how to execute some arbitrary code upon visiting an object.

    import contextlib

    import mdis.core
    import mdis.visitor

    class CustomVisitor(mdis.visitor.Visitor):
        @mdis.core.hook(int)
        @contextlib.contextmanager
        def visit_int(self, instance):
            print("entering int")
            yield (instance + 42)
            print("leaving int")

        @mdis.core.hook(str)
        @contextlib.contextmanager
        def visit_str(self, instance):
            print("entering str")
            yield f"!!!{instance}!!!"
            print("leaving str")

        @mdis.core.hook(object)
        @contextlib.contextmanager
        def visit_object(self, instance):
            print("entering object")
            yield instance
            print("leaving object")

    visitor = CustomVisitor()
    for item in (42, "cocojamboo", 1.5):
        with visitor(item) as result:
            print(result)

The following output is expected:

    entering int
    84
    leaving int
    entering str
    !!!cocojamboo!!!
    leaving str
    entering object
    1.5
    leaving object
