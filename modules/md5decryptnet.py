#
# -*- coding: utf-8 -*-
#
#  md5decryptnet.py
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

# Md5() Encrypt & Decrypt. Find out more on md5decrypt.net

from requests import post
from re import search

verbose_name = "Md5() Decrypt"

def do_request(hash_):    
    url = "https://md5decrypt.net/en/"
    data = {
        'hash': hash_,
        'decrypt': 'Decrypt',
    }
    
    m = search(r"{}\s+:\s+<b>(.+)</b>".format(hash_), (post(url, data)).text)
    if m:
        return {
            'success': True,
            'message': 'hash successfully cracked',
            'result': {
                'plaintext': m.group(1),
                'algorithm': 'md5',
            }
        }
    
    return {
        'success': False,
        'message': 'this hash cannot be cracked'
    }
