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

# $Id: RSASignedCookie.py,v 1.4 2005/02/11 20:37:23 grisha Exp $

from mod_python import Cookie

from Crypto.PublicKey import RSA

import sha
import marshal
import binascii

RSACookieError = 'RSACookieError'

class RSASignedCookie(Cookie.SignedCookie):

    """ A cookie that uses RSA to sign the cookie value. The nice
    thing about it is that one does not need to know a shared scret to
    verify the value, only the public key is necessary. """

    def rsa_sign(self, val):

        if not self.__data__["secret"]:
            raise RSACookieError, "Cannot sign without a RSA private key"

        digest = sha.new(val).digest()
        sig = self.__data__["secret"].sign(digest, open('/dev/urandom').read(32))

        return str(sig[0])


    def rsa_verify(self, val, sig, key):

        digest = sha.new(val).digest()
        return key.verify(digest, sig)


    def __str__(self):

        # if we do not have the private key, then we cannot present a string
        # representation, so we will fake something:
        if not self.__data__["secret"]:
            result = ["%s=%s:%s" % (self.name, 'NO RSA SIGNATURE SINCE NO PRIV KEY AVAILABLE',
                                    self.value)]
        else:
            result = ["%s=%s:%s" % (self.name, self.rsa_sign(self.name+self.value),
                                    self.value)]
        for name in self._valid_attr:
            if hasattr(self, name):
                if name in ("secure", "discard"):
                    result.append(name)
                else:
                    result.append("%s=%s" % (name, getattr(self, name)))
        return "; ".join(result)


    def unsign(self, key):


        try:
            sig, val = self.value.split(':', 1)
            sig = (long(sig),)
        except ValueError:
            raise RSACookieError, "Not an RSA Signed Cookie: %s=%s" % (self.name, self.value)
            
        if self.rsa_verify(self.name+val, sig, key):
            self.value = val
        else:
            raise RSACookieError, "Incorrectly Signed Cookie: %s=%s" % (self.name, self.value)

