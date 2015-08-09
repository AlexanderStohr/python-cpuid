import struct as _struct
# Try to import the native module.  Mask any import error.
try:
    from . import _cpuid
except ImportError:
    pass

def cpuid(level):
    return _cpuid.cpuid(level)

def vendor():
    eax, ebx, ecx, edx = _cpuid.cpuid(0)
    return _struct.pack("III", ebx, edx, ecx).strip('\0')

def stepping_id():
    return _cpuid.cpuid(1)[0] & 0xf
