from .dicts import to_dict


class Specable:
    """Mixin for (de)serialising objects with specable."""

    kind = None
    namespace = None

    # must be implemented by subclass
    def get_dict(self):
        raise NotImplementedError

    # may be implemented by sub-class
    @classmethod
    def _from_dict(cls, dct, **kwargs):
        return cls(**dct, **kwargs)

    # methods below should not be changed!

    def to_spec(self):
        return self.get_handle(), self.get_dict()

    def to_dict(self):
        return to_dict(*self.to_spec())

    @classmethod
    def from_dict(cls, dct, **kwargs):
        return cls._from_dict(dct, **kwargs)

    @classmethod
    def get_handle(cls):
        return f"{cls.get_namespace()}/{cls.get_kind()}"

    @classmethod
    def get_kind(cls):
        if cls.kind is None:
            return cls.__name__.lower()
        else:
            return kind

    @classmethod
    def get_namespace(cls):
        if cls.namespace is None:
            return cls.__module__.split(".")[0]
        else:
            return cls.namespace
