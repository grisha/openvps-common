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

# $Id: RSASignedCookie.py,v 1.1 2005/02/07 18:55:21 grisha Exp $

from mod_python import Cookie

from Crypto.PublicKey import RSA

import sha
import marshal
import binascii

class RSASignedCookie(Cookie.SignedCookie):

    """ A cookie that uses RSA to sign the cookie value. The nice
    thing about it is that one does not need to know a shared scret to
    verify the value, only the public key is necessary. """


    def rsa_sign(self, str):

        if not self.__data__["secret"]:
            raise CookieError, "Cannot sign without a RSA private key"

        digest = sha.new(str).digest()
        sig = self.__data__["secret"].sign(digest, open('/dev/urandom').read(32))

        return binascii.hexlify(marshal.dumps(sig))


    def rsa_verify(self, str, sig):

        if not self.__data__["secret"]:
            raise CookieError, "Cannot sign without an RSA (public) key"

        digest = sha.new(str).digest()
        return self.__data__["secret"].verify(digest, binascii.unhexlify(sig))


    def __str__(self):
        
        result = ["%s=%s:%s" % (self.name, self.rsa_sign(self.name+self.value),
                               self.value)]
        for name in self._valid_attr:
            if hasattr(self, name):
                if name in ("secure", "discard"):
                    result.append(name)
                else:
                    result.append("%s=%s" % (name, getattr(self, name)))
        return "; ".join(result)
