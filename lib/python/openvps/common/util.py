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

# $Id: util.py,v 1.1 2005/01/12 21:25:03 grisha Exp $

""" Misc. Utilities """

import random
import crypt

# salt is [a-zA-Z0-9./] according to crypt(3)
SALT_SET = range(ord('A'), ord('Z')+1) + \
           range(ord('a'), ord('z')+1) + \
           range(ord('0'), ord('9')+1) + \
           [ord('.'), ord('/')]

def hash_passwd(pw, md5=1, salt=None):
    """ Create a password hash """

    if not salt:

        # seeding from /dev/random should be better than
        # the default action of using current time
        random.seed(open('/dev/random').read(4))

    if md5: # md5

        if not salt:
            salt = ''
            for foo in range(8):
                i = random.choice(SALT_SET)
                salt = salt + chr(i)

        hash = crypt.crypt(pw, '$1$'+salt)

    else:  # DES                                                                                                                                          
        if not salt:

            salt = ''
            for foo in range(2):
                i = random.choice(SALT_SET)
                salt = salt + chr(i)

        hash = crypt.crypt(pw, salt)

    return hash

def check_passwd(passwd, pwhash):
    """ Check the password against the hash """

    ourhash = crypt.crypt(passwd, pwhash)

    return ourhash == pwhash
