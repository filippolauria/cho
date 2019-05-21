#
# -*- coding: utf-8 -*-
#
#  md5myaddrcom.py
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

# MD5.My-Addr.com is the Biggest MD5 database of Internet, size about
# 4,700,000,000 hashes.
#
# Find out more on md5.my-addr.com

from requests import post
from random import randint
from re import search

verbose_name = "MD5.My-Addr.com"

def do_request(hash_):    
    url = "http://md5.my-addr.com/md5_decrypt-md5_cracker_online/md5_decoder_tool.php"
    data = { 'md5': hash_, 'x': randint(11, 23), 'y': randint(11, 23) }
    response = post(url, data)
    
    m = search(
        r"<span\s+class='middle_title'>Hashed\s+string</span>:\s+(.+)</div>",
        response.text)
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
