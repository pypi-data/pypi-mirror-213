import random

import pytest

from pybinary.binary_types import ArrayTypes, Types
from pybinary.serializable import BinarySerializable


def test_simple_class():
    class Test(BinarySerializable):
        s8 = Types.s8
        u8 = Types.u8
        s16 = Types.s16
        u16 = Types.u16
        s32 = Types.s32
        u32 = Types.u32
        s64 = Types.s64
        u64 = Types.u64
        float = Types.float
        double = Types.double
    obj = Test()
    for field_name, field_value in obj._get_properties().items():
        value = random.randint(0, 255)
        setattr(obj, field_name, value)
        assert getattr(obj, field_name) == value


def test_simple_serialize():
    class Test(BinarySerializable):
        s8 = Types.s8
        u8 = Types.u8
        s16 = Types.s16
        u16 = Types.u16
        s32 = Types.s32
        u32 = Types.u32
        s64 = Types.s64
        u64 = Types.u64
        float = Types.float
        double = Types.double

    assert Test.size() == 1 + 1 + 2 + 2 + 4 + 4 + 8 + 8 + 4 + 8
    data = random.randbytes(Test.size())
    obj = Test.deserialize(data)
    assert obj.serialize() == data


def test_inheritance():
    class TestBase(BinarySerializable):
        s8 = Types.s8
        s16 = Types.s16

    class Test(TestBase):
        s32 = Types.s32

    assert Test.size() == 1 + 2 + 4
    data = random.randbytes(Test.size())
    obj = Test.deserialize(data)
    assert obj.serialize() == data


def test_name_collision():
    class TestBase(BinarySerializable):
        s8 = Types.s8
        s16 = Types.s16
        s32 = Types.s32

    with pytest.raises(TypeError):
        class Test(TestBase):
            s16 = Types.s32


def test_bytearray():
    size = random.randint(1, 100)

    class Test(BinarySerializable):
        bytearray = ArrayTypes.bytearray(size)

    assert Test.size() == size
    data = random.randbytes(size)
    obj =  Test.deserialize(data)
    assert obj.serialize() == data

