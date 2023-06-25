# SPDX-FileCopyrightText: © 2023 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""File check - fork of Russell Davis fileUtilities"""

import os

name = "checkfile"

def file_exists(filename):
    file_exists = False
    try:
        os.stat(filename)
        file_exists = True
    except OSError:
        file_exists = False
    
    return file_exists