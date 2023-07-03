# SPDX-FileCopyrightText: © 2023 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""USE THIS FILE TO GENERATE THE ENCRYPTED STRING
   AND THE KEY STRING. AFTER THEN, COPY BOTH IN THE
   FILE NAMED settings.toml IN THE FOLLOWING ORDER:
       - Encrypted: cryptk
       - KeyString: keystr
   THE core/keystrokes.py FILE WILL RECOGNIZE AS cryptk and keystr VARIABLES"""

import os
import core.skrcrypt as skrcrypt
from binascii import hexlify, unhexlify

keystring = hexlify(os.urandom(16)).decode()
inpstring = input("Write the string to encrypt(Max 16 characters): ")

print("This is the Key String: " + keystring)

crypted = skrcrypt.encrypt_string(keystring, inpstring)
print("This is the encrypted string: " + crypted)

decrypted = skrcrypt.decrypt_string(keystring, crypted)
