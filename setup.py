#!/usr/bin/env python

import platform
from distutils.core import setup, Extension

_cpuid_module = Extension(
    name = 'cpuid._cpuid',
    sources = ['cpuid/_cpuid.c'],
    extra_compile_args=[],
    extra_link_args=[],
)

setup(
    name='cpuid',
    version='1.0.0',
    author='Michael Mohr',
    author_email='akihana@gmail.com',
    description='Python CPUID library',
    ext_modules=[_cpuid_module],
    license='GPLv3',
    url='https://github.com/Rupan/python-cpuid',
    packages=['cpuid'],
)
