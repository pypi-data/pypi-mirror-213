import typing
from collections import OrderedDict
from io import BytesIO
import pybinary.binary_types as stypes
import logging



class _BinarySerializableSchema(type):
    def __new__(cls, name, bases, dct):
        def _create_setter(field) -> callable:
            def _setter(self, value) -> None:
                type_field = getattr(self, field)
                type_field.data = value
            return _setter

        def _create_getter(field) -> callable:
            def _getter(self) -> typing.Any:
                type_field = getattr(self, field)
                return type_field.data
            return _getter

        properties = OrderedDict()
        for field, value in dct.items():
            if isinstance(value, stypes._Type) or isinstance(value, stypes._ArrayType):
                properties[field] = value
        for field, value in properties.items():
            new_field_name = f'_{field}'
            dct[new_field_name] = value
            dct[field] = property(fset=_create_setter(new_field_name), fget=_create_getter(new_field_name))
        return super().__new__(cls, name, bases, dct)

    @classmethod
    def __prepare__(metacls, name, bases):
        return OrderedDict()


class BinarySerializable(metaclass=_BinarySerializableSchema):
    def serialize(self) -> bytes:
        result = b''
        for field, value in self.__properties.items():
            result += value.raw
        return result

    def __init_subclass__(cls, **kwargs):
        cls.__properties = cls._get_properties()

    @classmethod
    def _get_properties(cls) -> OrderedDict:
        inheritance_stack = []
        current_class = cls
        while issubclass(current_class, BinarySerializable) and current_class != BinarySerializable:
            inheritance_stack.append(current_class)
            current_class = current_class.__base__
        result = OrderedDict()
        while inheritance_stack:
            current_class = inheritance_stack.pop()
            for name, value in current_class.__dict__.items():
                if isinstance(value, stypes._Type) or isinstance(value, stypes._ArrayType):
                    if name in result:
                        raise TypeError(f"Duplicate field '{name}'")
                    result[name] = value
        return result

    @classmethod
    def size(cls):
        result = 0
        for name, value in cls.__properties.items():
            result += value.size
        return result

    @classmethod
    def deserialize(cls, data: bytes | BytesIO) -> object:
        expected_size = cls.size()
        if isinstance(data, bytes):
            if expected_size < len(data):
                logging.warning(f"Expected to deserialize {expected_size} bytes, {len(data)} bytes were provided. Ignoring trailing bytes")
            elif expected_size > len(data):
                raise ValueError(f"Expected to deserialize {expected_size} bytes, {len(data)} bytes were provided")
            data_stream = BytesIO(data)
        else:
            data_stream = data
        result = cls()
        properties = cls.__properties
        for name, value in properties.items():
            field = getattr(result, name)
            field.raw = data_stream.read(field.size)
        return result
