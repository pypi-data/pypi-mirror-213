
#include "gpu_control.h"

#ifdef _DEBUG
#undef _DEBUG
#include <python.h>
#define _DEBUG
#else
#include <python.h>
#endif

// Wrapper for get_temperature function
static PyObject* gpu_get_temperature(PyObject* self, PyObject* args) {
    int temp = get_temperature();
    return PyLong_FromLong(temp);
}

// Wrapper for set_fan_speed function
static PyObject* gpu_set_fan_speed(PyObject* self, PyObject* args) {
    int speed;
    if (!PyArg_ParseTuple(args, "i", &speed))
        return NULL;
    int result = set_fan_speed(speed);
    return PyLong_FromLong(result);
}

// Wrapper for get_fan_speed function
static PyObject* gpu_get_fan_speed(PyObject* self, PyObject* args) {
    int speed = get_fan_speed();
    return PyLong_FromLong(speed);
}

// Define methods in module
static PyMethodDef GpuMethods[] = {
    {"get_temperature",  gpu_get_temperature, METH_NOARGS, "Get the GPU temperature."},
    {"set_fan_speed",  gpu_set_fan_speed, METH_VARARGS, "Set the GPU fan speed."},
    {"get_fan_speed",  gpu_get_fan_speed, METH_NOARGS, "Get the GPU fan speed."},
    {NULL, NULL, 0, NULL}
};

// Define module
static struct PyModuleDef gpu_module = {
    PyModuleDef_HEAD_INIT,
    "gpu_control",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    GpuMethods
};

// Init function
PyMODINIT_FUNC PyInit_gpu_control(void) {
    return PyModule_Create(&gpu_module);
}
