# pybinary
A simple binary serializer/deserializer in pure python.

## Limitations
Variable-sized fields are not supported. No size check on assignment for the most of the types.

## Installation 
Download the repository and build from the sources:
```
python3 ./setup.py build
python3 ./setup.py install
```

## Examples
### ELF64 header
Spec taken from https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html

```
class Elf64_Ehdr(BinarySerializable):
    e_ident = ArrayTypes.bytearray(16)
    e_type = Types.u16
    e_machine = Types.u16
    e_version = Types.u32
    e_entry = Types.u64
    e_phoff = Types.u64
    e_shoff = Types.u64
    e_flags = Types.u32
    e_ehsize = Types.u16
    e_phentsize = Types.u16
    e_phnum = Types.u16
    e_shentsize = Types.u16
    e_shnum = Types.u16
    e_shstrndx  = Types.u16


header = Elf64_Ehdr.deserialize(input_stream_or_bytes) # deserialize header
header.e_phnum += 1 # update any field
header.serialize() # serialize and get updated bytes
...

```

### CPIO Newc ACII Format Archive 

Spec taken from https://manpages.ubuntu.com/manpages/bionic/man5/cpio.5.html

[Code here](https://github.com/lim8en1/pybinary/blob/main/examples/cpio.py)

