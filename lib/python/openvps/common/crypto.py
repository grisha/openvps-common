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

# $Id: crypto.py,v 1.1 2005/02/05 05:28:18 grisha Exp $

""" Crypto Functions """

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

import marshal
import binascii
import os

def random(n):

    return open('/dev/urandom').read(n)

def genkey(bits=512):

    return RSA.generate(bits, random)

def rsa2str(rsa):
    """ Convert and RSA key to an ASCII str """

    key = []
    for k in rsa.keydata:
        if hasattr(rsa, k):
            key.append(getattr(rsa, k))

    return marshal.dumps(tuple(key))

def str2rsa(str):
    """ Convert an rsa2str() generated string back to RSA key """

    return RSA.construct(marshal.loads(str))

def pad(str, block_size, pchar=' '):
    """ Pad string up to a block_size mltiple with pachar"""

    return str + (pchar * (block_size - (len(str) % block_size)))

def encrypt(str, passphrase):
    """ Encrypt a string """

    aes  = AES.new(pad(passphrase, 32), AES.MODE_CBC)

    # need salt to make sure output is different every time
    salt = random(4)

    # the reason it is hexlified is to be able easily strip
    # blanks upon decryption (even though this doubles the string,
    # but this is good enough for us)
    hstr = pad(binascii.hexlify(salt + str), AES.block_size)
    
    c_text = aes.encrypt(hstr)

    return salt + c_text

def decrypt(str, passphrase):
    """ Decrypt a string """

    aes  = AES.new(pad(passphrase, 32), AES.MODE_CBC)

    msg = aes.decrypt(pad(str[4:], AES.block_size))

    # since the string was hexlified before encryption, it cannot
    # contain blanks, so we use split() to strip trailing garbage,
    # if any.
    msg = binascii.unhexlify(msg.split()[0])
    
    if msg[:4] != str[:4]:
        # salt doesn't mach, bad password
        return None

    return msg[4:]

def save_key(key, path, passphrase=None):

    str_key = rsa2str(key)

    if passphrase:
        str_key = encrypt(str_key, passphrase)

    if os.path.exists(path):
        os.unlink(path) 
    open(path, 'wb').write(str_key)

def load_key(path, passphrase=None):

    str_key = open(path, 'rb').read()

    try:
        if passphrase:
            str_key = decrypt(str_key, passphrase)

        key = str2rsa(str_key)
        
    except (ValueError, TypeError):
        return None

    return key
