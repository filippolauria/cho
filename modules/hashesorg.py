#
# -*- coding: utf-8 -*-
#
#  hashesorg.py
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

# Hashes.org is a free online hash resolving service incorporating many 
# unparalleled techniques. It is obvious that legacy methods of hash cracking
# are both time consuming and wasteful of resources...
#
# Find out more on Hashes.org

from requests import get

verbose_name = "Hashes.org"
api_key = None

def do_check_configuration(config):
    global api_key
    
    if not verbose_name in config:
        return {
            'success': False,
            'message': "section '{}' not found in configuration file."
        }
    
    api_key = config[verbose_name].get("api_key")
    if api_key:
        return {
            'success': True,
            'message': 'the module seems to be well configured.'
        }
    

    return {
        'success': False,
        'message': 'have you configured API Key?'
    }
    

def do_request(hash_):
    
    if not api_key:
        return {
            'success': False,
            'message': 'have you configured API Key?'
        }
    
    query = "https://hashes.org/api.php?key={}&query={}".format(
        api_key, hash_)
    
    
    response = get(query).json()
    if response["status"] != "success":
        return {
            'success': False,
            'message': 'an error occurred'
        }
    
    if not response["result"][hash_]:
        return {
            'success': False,
            'message': 'this hash cannot be cracked'
        }
    
    return {
        'success': True,
        'message': 'hash successfully cracked',
        'result': {
            'plaintext': response["result"][hash_]['plain'],
            'algorithm': response["result"][hash_]['algorithm'],
        }
    }

