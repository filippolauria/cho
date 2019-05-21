#
# -*- coding: utf-8 -*-
#
#  nitrxgen.py
#  
#  Copyright 2019 Filippo Lauria
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# NITRXGEN has a look-up tool for typical unsalted MD5 cryptographic hashes.
# The database currently contains 1.1+ trillion passwords.
#
# Find out more on NITRXGEN.net

from requests import get

verbose_name = "NITRXGEN"

def do_request(hash_):
    response = get("http://www.nitrxgen.net/md5db/{}.json".format(hash_))
    
    if response.text:
        response = response.json()    
        if response["result"]["found"]:
            return {
                'success': True,
                'message': 'hash successfully cracked',
                'result': {
                    'plaintext': response["result"]["pass"],
                    'algorithm': 'md5',
                }
            }
    
    return {
        'success': False,
        'message': 'this hash cannot be cracked'
    }
