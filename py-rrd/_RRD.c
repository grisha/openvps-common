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
 * $Id: _RRD.c,v 1.1 2004/12/21 21:07:06 grisha Exp $
 *
 */

#include <Python.h>
#include <rrd.h>

#include <stdio.h>

static void
free_string_array(char **array, int count)
{
  int i;
  for (i = 0; i < count; i++)
    PyMem_Free(array[i]);
  PyMem_DEL(array);
}

static PyObject * 
_RRD_call(PyObject *self, PyObject *args)
{
  char *action;
  PyObject *argv;
  char **argvlist;
  int i, argc, rc;
  PyObject *(*getitem)(PyObject *, int);

  if (!PyArg_ParseTuple(args, "sO", &action, &argv))
    return NULL;

  if (PyList_Check(argv)) {
    argc = PyList_Size(argv);
    getitem = PyList_GetItem;
  }
  else if (PyTuple_Check(argv)) {
    argc = PyTuple_Size(argv);
    getitem = PyTuple_GetItem;
  }
  else {
    PyErr_SetString(PyExc_TypeError, "argument must be a tuple or list");
    return NULL;
  }
  
  if (argc == 0) {
    PyErr_SetString(PyExc_ValueError, "argument must not be empty");
    return NULL;
  }

  argvlist = PyMem_NEW(char *, argc+1);
  if (argvlist == NULL) {
    return PyErr_NoMemory();
  }

  for (i = 0; i < argc; i++) {
    if (!PyArg_Parse((*getitem)(argv, i), "s", &argvlist[i])) {
      free_string_array(argvlist, i);
      PyErr_SetString(PyExc_TypeError,
		      "argument must contain only strings");
      return NULL;
    }
  }
  argvlist[argc] = NULL;

  /* it's important to reset getopt state */
  opterr = 0;
  optind = 0;

  if (!strcmp("create", action)) 
    rc = rrd_create(argc, argvlist);
  else if (!strcmp("update", action))
      rc = rrd_update(argc, argvlist);
  else if (!strcmp("restore", action))
    rc = rrd_restore(argc, argvlist);
  else if (!strcmp("dump", action))
    rc = rrd_dump(argc, argvlist);
  else if (!strcmp("tune", action))
    rc = rrd_tune(argc, argvlist);
  else if (!strcmp("last", action))
    rc = rrd_last(argc, argvlist);
  else if (!strcmp("resize", action))
    rc = rrd_resize(argc, argvlist);
  else {
      free_string_array(argvlist, i);
      PyErr_SetString(PyExc_TypeError,
		      "invalid action");
      return NULL;
  }

  if (rc == -1) {
    PyErr_SetString(PyExc_ValueError,
		    rrd_get_error());
    rrd_clear_error();
    return NULL;
  }

  return PyLong_FromLong(rc);
}

// XXX need to implement graph, fetch and xport

struct PyMethodDef _RRD_module_methods[] = {
    {"call",     (PyCFunction) _RRD_call,   METH_VARARGS},
    {NULL, NULL}
};

void init_RRD(void)
{
    Py_InitModule("_RRD", _RRD_module_methods);
}
