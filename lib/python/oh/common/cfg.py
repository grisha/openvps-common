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

# $Id: cfg.py,v 1.3 2004/12/28 03:29:44 grisha Exp $

# These config elements are common between host and admin

MON_TARGET_PORT = 2004

# These are the definitions of the data points that the monitor agent
# collects and sends out. The definitions and the order here need to
# match those on the receiving end becuase the receiver will create an
# RRD database based on this defintion. On the host side only the
# 'name' and the order of elements matter.

HB = 300 # default heart beat

# (name, rrd_type, hbeat, min, max)
MON_DATA_DEF = [('hostname', None, None, None, None),
                ('cpu_loadavg1', 'gauge', HB, 0, 'U'),
                ('nprocs', 'gauge', HB, 0, 'U'),
                ('mem_MemTotal', 'gauge', 86400, 0, 'U'),
                ('mem_MemFree', 'gauge', HB, 0, 'U'),
                ('mem_Cached', 'gauge', HB, 0, 'U'),
                ('mem_Active', 'gauge', HB, 0, 'U'), 
                ('mem_SwapTotal', 'gauge', 86400, 0, 'U'),
                ('mem_SwapFree', 'gauge', HB, 0, 'U'),
                ('forks', 'gauge', HB, 1, 'U'),
                ('net_eth0_rx_bytes', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth0_tx_bytes', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth0_packets', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth0_errors', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth0_drop', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth1_rx_bytes', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth1_tx_bytes', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth1_packets', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth1_errors', 'counter', HB, 0, 0xFFFFFF00L),
                ('net_eth1_drop', 'counter', HB, 0, 0xFFFFFF00L),
                ('disk_root_used', 'gauge', HB, 0, 'U'),
                ('disk_var_used', 'gauge', HB, 0, 'U'),
                ('disk_tmp_used', 'gauge', HB, 0, 'U'),
                ('disk_backup_used', 'gauge', HB, 0, 'U'),
                ('disk_vservers_used', 'gauge', HB, 0, 'U'),
                ('disk_root_free', 'gauge', HB, 0, 'U'),
                ('disk_var_free', 'gauge', HB, 0, 'U'),
                ('disk_tmp_free', 'gauge', HB, 0, 'U'),
                ('disk_backup_free', 'gauge', HB, 0, 'U'),
                ('disk_vservers_free', 'gauge', HB, 0, 'U'),
                ('disk_a_reads', 'counter', HB, 0, 0xFFFFFF00L),
                ('disk_a_writes', 'counter', HB, 0, 0xFFFFFF00L),
                ('disk_b_reads', 'counter', HB, 0, 0xFFFFFF00L),
                ('disk_b_writes', 'counter', HB, 0, 0xFFFFFF00L),
                ('ipc_shmall', 'gauge', HB, 0, 0xFFFFFF00L),
                ('ipc_totshm', 'gauge', HB, 0, 0xFFFFFF00L),
                ('ipc_semmns', 'gauge', HB, 0, 0xFFFFFF00L),
                ('ipc_totsem', 'gauge', HB, 0, 0xFFFFFF00L),
                ]



