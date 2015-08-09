import struct as _struct
# Try to import the native module.  Mask any import error.
try:
    from . import _cpuid
except ImportError:
    pass

# Add this to the level parameter in order to get extended CPUID information
EXTENDED_OFFSET = 0x80000000

# Method definitions
def cpuid(level):
    return _cpuid.cpuid(level)

def vendor():
    eax, ebx, ecx, edx = _cpuid.cpuid(0)
    return _struct.pack("III", ebx, edx, ecx).strip('\0')

def stepping_id():
    return _cpuid.cpuid(1)[0] & 0xf

def model():
    a = _cpuid.cpuid(1)[0]
    model_number = (a >> 4) & 0xf
    extended_model = (a >> 16) & 0xf
    return (extended_model << 4) + model_number

def family():
    a = _cpuid.cpuid(1)[0]
    family_code = (a >> 8) & 0xf
    extended_family = (a >> 20) & 0xff
    return extended_family + family_code

def processor_type():
    return (_cpuid.cpuid(1)[0] >> 12) & 0x3

def brand_id():
    return _cpuid.cpuid(1)[1] & 0xff

def brand_string():
    a = cpuid(EXTENDED_OFFSET)
    if a[0] < (EXTENDED_OFFSET | 0x4):
        raise NotImplementedError("Brand string is not supported by this CPU")
    segments = [_struct.pack("IIII", *_cpuid.cpuid(EXTENDED_OFFSET | k)) for k in (0x2, 0x3, 0x4)]
    return str(''.join([s.decode('utf-8').strip('\0') for s in segments]))
