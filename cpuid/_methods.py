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
    return _struct.pack("III", ebx, edx, ecx)

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
    return ''.join([s.decode('utf-8').strip('\0') for s in segments])

def features():
    info = cpuid(1)
    return [key for key, reg, bit in _feat_table if info[reg] & (1 << bit)]

_feat_table = [
    ("FPU", 3, 0),
    ("VME", 3, 1),
    ("DE", 3, 2),
    ("PSE", 3, 3),
    ("TSC", 3, 4),
    ("MSR", 3, 5),
    ("PAE", 3, 6),
    ("MCE", 3, 7),
    ("CX8", 3, 8),
    ("APIC", 3, 9),
    ("SEP", 3, 11),
    ("MTRR", 3, 12),
    ("PGE", 3, 13),
    ("MCA", 3, 14),
    ("CMOV", 3, 15),
    ("PAT", 3, 16),
    ("PSE36", 3, 17),
    ("PSN", 3, 18),
    ("CLFLSH", 3, 19),
    ("DS", 3, 21),
    ("ACPI", 3, 22),
    ("MMX", 3, 23),
    ("FXSR", 3, 24),
    ("SSE", 3, 25),
    ("SSE2", 3, 26),
    ("SS", 3, 27),
    ("HTT", 3, 28),
    ("TM", 3, 29),
    ("PBE", 3, 31),
    ("SSE3", 2, 0),
    ("PCLMULDQ", 2, 1),
    ("DTES64", 2, 2),
    ("MONITOR", 2, 3),
    ("DSCPL", 2, 4),
    ("VMX", 2, 5),
    ("SMX", 2, 6),
    ("EST", 2, 7),
    ("TM2", 2, 8),
    ("SSE3", 2, 9),
    ("CNXTID", 2, 10),
    ("CX16", 2, 13),
    ("XTPR", 2, 14),
    ("PDCM", 2, 15),
    ("DCA", 2, 18),
    ("SSE4_1", 2, 19),
    ("SSE4_2", 2, 20),
    ("X2APIC", 2, 21),
    ("MOVBE", 2, 22),
    ("POPCNT", 2, 23),
    ("AES", 2, 25),
    ("XSAVE", 2, 26),
    ("OSXSAVE", 2, 27),
]
