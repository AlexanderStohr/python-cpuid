#!/usr/bin/python

from __future__ import print_function
import cpuid

if __name__ == "__main__":
    print("Vendor:", cpuid.vendor())
    print("Stepping ID:", cpuid.stepping_id())
    print("Model:", hex(cpuid.model()))
    print("Family:", cpuid.family())
    print("Processor Type:", cpuid.processor_type())
    print("Brand ID:", hex(cpuid.brand_id()))
    print("Brand String:", cpuid.brand_string())
    print("Features:", cpuid.features())

    eax, ebx, ecx, edx = cpuid.cpuid(1, 0)
    # http://www.flounder.com/cpuid_explorer2.htm
    cpu_sig = {
        'Stepping ID': (eax >> 0x00) & 0x0f,
        'Model ID': (eax >> 0x04) & 0x0f,
        'Family ID': (eax >> 0x08) & 0x0f,
        'Processor Type': (eax >> 0x0c) & 0x03,  # Reserved on AMD
        'Reserved2': (eax >> 0x0e) & 0x03,
        'Extended Model': (eax >> 0x10) & 0x0f,
        'Extended Family': (eax >> 0x14) & 0xff,
        'Reserved': (eax >> 0x1c) & 0x0f,
    }
    print("Signature:", cpu_sig)
