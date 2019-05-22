#
# -*- coding: utf-8 -*-
#
#  hashtoolkit.py
#  
#  Copyright 2019 Filippo Lauria (filippo.lauria@iit.cnr.it)
#                 Gruppo Reti IIT-CNR (grupporeti-dev@iit.cnr.it)
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

# Hash Toolkit Hash Decrypter enables you to decrypt / reverse a hash in
# various formats into their original text.
#
# Find out more on hashtoolkit.com

from requests import get
from re import search

verbose_name = "Hash Toolkit"

def do_request(hash_):    
    m = search(r"<span\s+title=\"decrypted\s+(\w+)\s+hash\">(.+)</span>", (
            get("https://hashtoolkit.com/reverse-hash?hash={}".format(
                hash_))).text)
    if m:
        return {
            'success': True,
            'message': 'hash successfully cracked',
            'result': {
                'plaintext': m.group(2),
                'algorithm': m.group(1),
            }
        }
    
    return {
        'success': False,
        'message': 'this hash cannot be cracked'
    }
