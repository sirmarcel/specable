from importlib import import_module

from .specable import Specable
from .dicts import parse_dict
from .inout import read_yaml, write_yaml


class Interface:
    def __init__(self, default_namespace, collection, allow_stubs=False):
        """

        Args:
            default_namespace: module to search if no namespace is given
            collection: name of the list of classes at module level to search
            allow_stubs: if True, allow "handle" by itself as shorthand
                for {"handle": {}}

        """

        self.default_namespace = default_namespace
        self.collection = collection
        self.allow_stubs = allow_stubs

        self.namespaces = {}

    def to_spec(self, specable):
        return specable.to_spec()

    def to_dict(self, specable):
        return specable.to_dict()

    def from_spec(self, handle, payload, **kwargs):
        cls = self.get_class(handle)
        return cls.from_dict(payload, **kwargs)

    def from_dict(self, dct, **kwargs):
        if isinstance(dct, Specable):
            return dct
        else:
            handle, payload = parse_dict(dct, allow_stubs=self.allow_stubs)
            return self.from_spec(handle, payload)

    def from_yaml(self, filename, **kwargs):
        dct = read_yaml(filename)

        return self.from_dict(dct, **kwargs)

    def to_yaml(self, filename, specable):
        dct = specable.to_dict()

        write_yaml(filename, dct)

    def get_class(self, handle):
        namespace, kind = self.parse_handle(handle)

        if namespace not in self.namespaces:
            self.import_namespace(namespace)

        # TODO: fail with meaningful exception
        return self.namespaces[namespace][kind]

    def parse_handle(self, handle):
        if "/" in handle:
            namespace, kind = handle.split("/")
        else:
            namespace = self.default_namespace
            kind = handle

        return namespace, kind

    def import_namespace(self, namespace):
        module = import_module(namespace)
        classes = getattr(module, self.collection)

        self.namespaces[namespace] = {cls.get_kind(): cls for cls in classes}
