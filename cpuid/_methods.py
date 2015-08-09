# Try to import the native module.  Mask any import error.
try:
    from . import _cpuid
except ImportError:
    pass

def cpuid(level):
    return _cpuid.cpuid(level)

