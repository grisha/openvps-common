#
# Copyright 2004 OpenHosting, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# XXX This file may need to be GPL'd

# $Id: setup.py,v 1.1 2004/12/21 21:07:06 grisha Exp $

from distutils.core import setup, Extension

import os

setup(name="pyrrd",
      version="0.01",
      description="(yeat another) Python RRD interface",
      author="OpenVPS Project",
      author_email="dev@openvps.org",
      url="http://www.openvps.org/",
      py_modules=['RRD'],
      ext_modules=[Extension("_RRD",
                             ["_RRD.c"],
                             include_dirs=['.', '/usr/local/include'],
                             libraries=['rrd'],
                             library_dirs=['/usr/local/lib'],
                             extra_compile_args=['-g'],
                             )
                   ]
      )

# makes emacs go into python mode
### Local Variables:
### mode:python
### End:
