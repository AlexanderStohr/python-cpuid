/*
  _cpuid.c: Python native code allowing access to CPUID data on x86.
  Copyright (C) 2015 Michael Mohr <akihana@gmail.com>

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <Python.h>

#if defined(__i386__) || defined(__x86_64__)

#include <stdio.h>
#include <sched.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <cpuid.h>

static PyObject *_cpuid_cpuid(PyObject *module, PyObject *args) {
    pid_t pid;
    cpu_set_t saved, target;
    int affinity_ret, cpuid_ret;
    int cpu_num = 0;
    unsigned int level = 0;
    unsigned int eax, ebx, ecx, edx;

    if(!PyArg_ParseTuple(args, "I|i", &level, &cpu_num))
        return NULL;

    /* Retrieve current CPU affinity so it can later be restored */
    pid = syscall(__NR_gettid);
    if(sched_getaffinity(pid, sizeof(cpu_set_t), &saved) != 0) {
        PyErr_SetString(PyExc_RuntimeError, "Unable to get CPU affinity");
        return NULL;
    }

    /* Set CPU affinity to one of the CPU cores (defaults to 0) */
    CPU_ZERO(&target);
    CPU_SET(cpu_num, &target);
    if(sched_setaffinity(pid, sizeof(cpu_set_t), &target) != 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    /* Retrieve CPUID data */
    cpuid_ret = __get_cpuid(level, &eax, &ebx, &ecx, &edx);
    /* Unconditionally attempt to restore original CPU affinity */
    affinity_ret = sched_setaffinity(pid, sizeof(cpu_set_t), &saved);

    /* Raise exception on error */
    if(cpuid_ret != 1) {
        PyErr_SetString(PyExc_RuntimeError, "CPUID level not supported");
        return NULL;
    }

    if(affinity_ret != 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return Py_BuildValue("{s:I,s:I,s:I,s:I}",
        "eax", eax, "ebx", ebx, "ecx", ecx, "edx", edx);
}

#else

static PyObject *_cpuid_cpuid(PyObject *module, PyObject *args) {
    PyErr_SetString(PyExc_NotImplementedError, "CPUID is only supported on x86");
    return NULL;
}

#endif

static PyMethodDef _cpuid_methods[] = {
    { "cpuid", _cpuid_cpuid, METH_VARARGS, "Retrieve CPUID information from a given CPU"},
    { NULL, NULL, 0, NULL},
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_cpuid",            /* m_name */
    "CPUID info",        /* m_doc */
    -1,                  /* m_size */
    _cpuid_methods,      /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
};

PyMODINIT_FUNC PyInit__cpuid(void) {
    PyObject *m;

    m = PyModule_Create(&moduledef);
    if(m == NULL)
        return NULL;
    return m;
}

#else

PyMODINIT_FUNC init_cpuid(void) {
    (void)Py_InitModule3("_cpuid", _cpuid_methods, "CPUID info");
}

#endif

