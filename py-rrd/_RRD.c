/*
 * Copyright 2004 Apache Software Foundation 
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you
 * may not use this file except in compliance with the License.  You
 * may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.  See the License for the specific language governing
 * permissions and limitations under the License.
 *
 * $Id: _RRD.c,v 1.2 2005/01/25 20:41:25 grisha Exp $
 *
 */

#include <Python.h>
#include <rrd.h>

#include <stdio.h>
#include <math.h>

char** parse_args(PyObject *args, int *argc) {

    /* take a Python args object, return a C-style
       argc and argv */
    
    char **argv;
    int i;
    PyObject *py_argv;
    PyObject *(*getitem)(PyObject *, int);

    if (!PyArg_ParseTuple(args, "O", &py_argv))
        return NULL;

    if (PyList_Check(py_argv)) {
        *argc = PyList_Size(py_argv);
        getitem = PyList_GetItem;
    }
    else if (PyTuple_Check(py_argv)) {
        *argc = PyTuple_Size(py_argv);
        getitem = PyTuple_GetItem;
    }
    else {
        PyErr_SetString(PyExc_TypeError, "argument must be a tuple or list");
        return NULL;
    }
  
    if (*argc == 0) {
        PyErr_SetString(PyExc_ValueError, "argument must not be empty");
        return NULL;
    }

    argv = PyMem_NEW(char *, *argc+1);
    if (argv == NULL) {
        PyErr_NoMemory();
        return NULL;
    }

    for (i = 0; i < *argc; i++) {
        if (!PyArg_Parse((*getitem)(py_argv, i), "s", &argv[i])) {
            PyMem_DEL(argv);
            PyErr_SetString(PyExc_TypeError,
                            "argument must contain only strings");
            return NULL;
        }
    }
    argv[*argc] = NULL;

    /* it's important to reset getopt state */
    opterr = 0;
    optind = 0;
    
    return argv;
}

static PyObject * _RRD_fetch(int argc, char **argv) {

    int rc, i, row_cnt;
    time_t start, end;
    unsigned long step, count;
    char **names;
    rrd_value_t *data;

    PyObject *result;
    PyObject *temp_obj;

    rc = rrd_fetch(argc, argv, &start, &end, &step, &count,
                   &names, &data);

    if (rc == -1) {
        PyMem_DEL(argv);
        PyErr_SetString(PyExc_ValueError,
                        rrd_get_error());
        rrd_clear_error();
        return NULL;
    }

    /*
     * Build ((start, end, step), (name1, name2, ...), [(data1, data2, ..), ...])
     *
     */

    result = PyTuple_New(3);
    if (! result) {
        PyMem_DEL(argv);
        return NULL;
    }

    /* (start, end, step) */

    temp_obj = Py_BuildValue("(i,i,i)", start, end, step);
    if (! temp_obj)
        goto error;
    PyTuple_SET_ITEM(result, 0, temp_obj);

    /* (name1, name2, ...) */

    temp_obj = PyTuple_New(count);
    if (! temp_obj) 
        goto error;
    PyTuple_SET_ITEM(result, 1, temp_obj);

    for (i = 0; i < count; i++) {
        PyObject *str = PyString_FromString(names[i]);
        if (! str)
            goto error;
        PyTuple_SET_ITEM(temp_obj, i, str);
    }
    
    /* [(data1, data2, ...) */

    row_cnt = ((end - start) / step) + 1;

    temp_obj = PyList_New(row_cnt);
    if (! temp_obj) 
        goto error;
    PyTuple_SET_ITEM(result, 2, temp_obj);

    for (i=0; i < row_cnt; i++) {
        int ii;
        PyObject *tup = PyTuple_New(count);
        if (! tup) 
            goto error;
        PyList_SET_ITEM(temp_obj, i, tup);
        for (ii=0; ii<count; ii++) {
            rrd_value_t val = data[i+ii];
            if (isnan(val)) {
                Py_INCREF(Py_None);
                PyTuple_SET_ITEM(tup, ii, Py_None);
            }
            else { 
                PyObject *obj = PyFloat_FromDouble((double)val);
                if (! obj) 
                    goto error;
                PyTuple_SET_ITEM(tup, ii, obj);
            } 
        }
    }

    PyMem_DEL(argv);
    return result;

 error:

    Py_DECREF(result);
    PyMem_DEL(argv);
    return NULL;
}

static PyObject * _RRD_call(PyObject *self, PyObject *args) {

    char **argv;
    int argc, rc;

    argv = parse_args(args, &argc);
    if (!argv)
        return NULL;

    if (!strcmp("create", argv[0])) 
        rc = rrd_create(argc, argv);
    else if (!strcmp("update", argv[0]))
        rc = rrd_update(argc, argv);
    else if (!strcmp("restore", argv[0]))
        rc = rrd_restore(argc, argv);
    else if (!strcmp("dump", argv[0]))
        rc = rrd_dump(argc, argv);
    else if (!strcmp("tune", argv[0]))
        rc = rrd_tune(argc, argv);
    else if (!strcmp("last", argv[0]))
        rc = rrd_last(argc, argv);
    else if (!strcmp("resize", argv[0]))
        rc = rrd_resize(argc, argv);
    else if (!strcmp("fetch", argv[0])) {
        return _RRD_fetch(argc, argv);
    }
    else {
        PyMem_DEL(argv);
        PyErr_SetString(PyExc_TypeError,
                        "invalid action");
        return NULL;
    }
    
    if (rc == -1) {
        PyMem_DEL(argv);
        PyErr_SetString(PyExc_ValueError,
                        rrd_get_error());
        rrd_clear_error();
        return NULL;
    }
    
    PyMem_DEL(argv);
    return PyLong_FromLong(rc);
}


// XXX need to implement graph, fetch and xport

struct PyMethodDef _RRD_module_methods[] = {
    {"call",     (PyCFunction) _RRD_call,     METH_VARARGS},
    {NULL, NULL}
};

void init_RRD(void) {
    Py_InitModule("_RRD", _RRD_module_methods);
}
