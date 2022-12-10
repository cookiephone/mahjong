from functools import wraps


class InheritDecoratorMixin:

    @staticmethod
    def inheritable_decorator(decorator):
        @wraps(decorator)
        def wrap(func):
            @decorator
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            wrapper.inherit_decorator = wrap
            return wrapper
        return wrap

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls._decorator_registry = getattr(cls, "_decorator_registry", {})
        for name, obj in cls.__dict__.items():
            if getattr(obj, "inherit_decorator", False) and not name in cls._decorator_registry:
                cls._decorator_registry[name] = obj.inherit_decorator
        for name, decorator in cls._decorator_registry.items():
            if name in cls.__dict__ and getattr(getattr(cls, name), "inherit_decorator", None) != decorator:
                setattr(cls, name, decorator(cls.__dict__[name]))