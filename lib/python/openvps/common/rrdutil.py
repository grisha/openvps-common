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

# $Id: rrdutil.py,v 1.2 2005/01/18 00:05:20 grisha Exp $

""" RRDTool related utilities """


RRDTOOL = '/usr/bin/rrdtool' # XXX needs to be determined by configure
RRDSTEP = 60

import time
import os
import tempfile
import commands

def period_total(rrd, start, end):

    cmd = '%s fetch %s AVERAGE -s %d -e %d' % (RRDTOOL, rrd, start, end)
    pipe = os.popen(cmd, 'r')

    tin, tout = 0.0, 0.0

    for line in pipe:
        line = line.strip()
        if line and not (line.startswith('in') or line.startswith('ti')):
            input, output = line.split()[1:]
            if input != 'nan':
                tin += float(input)
            if output != 'nan':
                tout += float(output)
    pipe.close()

    return long(tin*RRDSTEP), long(tout*RRDSTEP)

def next_month(year, month):

    if month == 12:
        return year+1, 1
    else:
        return year, month+1

def prev_month(year, month):
    if month == 1:
        return year-1, 12
    else:
        return year, month-1

def month_total(rrd, year, month):
    """ Get total for the month
        year must be in YYYY format
    """

    # beginning of the month
    s = time.mktime(time.strptime('%d%02d' % (year, month), '%Y%m'))

    eyear, emonth = next_month(year, month)

    e = time.mktime(time.strptime('%d%02d' % (eyear, emonth), '%Y%m')) - 86400

    return period_total(rrd, s, e)

def graph(rrd, back=86400, title='', width=400, height=100):
    """ Make an RRD graph. The caller is responsible for
    deleting the returned path """
    
    tfile, tpath = tempfile.mkstemp('.gif', 'oh')
    os.close(tfile)

    cmd = '%s graph %s --start -%d ' % (RRDTOOL, tpath, back)
    cmd += '--title "%s" ' % title
    cmd += '-w %d ' % width
    cmd += '-h %d ' % height
    cmd += 'DEF:in=%s:in:AVERAGE ' % rrd
    cmd += 'DEF:out=%s:out:AVERAGE ' % rrd
    cmd += 'CDEF:inbits=in,8,* ' \
           'CDEF:outbits=out,8,* ' \
           'AREA:inbits#00FF00:"bps in" ' \
           'LINE1:outbits#0000FF:"bps out" '
    commands.getoutput(cmd)

    return tpath