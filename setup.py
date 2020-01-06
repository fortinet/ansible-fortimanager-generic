#!/usr/bin/python
from __future__ import absolute_import, division, print_function
# Copyright 2020 Fortinet, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import shutil

def get_fortimanager_module_directory():
    try:
        import ansible.modules.network.fortimanager as fmgr
        return fmgr.__path__[0]
    except ImportError as e:
        print('Please make sure ansible is installed') 
        sys.exit(1)

def main():
    mod_dir = get_fortimanager_module_directory()
    shutil.copyfile('./fmgr_generic.py', mod_dir + '/fmgr_generic.py')
    try:
        import ansible.modules.network.fortimanager.fmgr_generic
    except ImportError as e:
        print('Fail to import fmgr_generic module')
        sys.exit(2)

if __name__ == '__main__':
    main()
