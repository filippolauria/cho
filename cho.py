#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  cho.py
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

import argparse
from importlib import import_module
import os
import re
import configparser

modules = {}
max_key_len = 0

def hash_validate(value):
    if not re.match('^[0-9a-fA-F]+$', value):
        raise argparse.ArgumentTypeError(
            "Invalid hash value (only hex-digits allowed)")
    
    return value

def print_(color, module_name, message):
    global max_key_len
    
    
    padding_len = max_key_len - len(module_name)
    padded_name = (' '*padding_len) + module_name if padding_len > 0 else module_name
    
    print(("{}{}: {}".format(color, padded_name, message)) + '\033[0m')

class colorprint():
    failure = lambda x,y: print_('\033[31m', x, y)
    success = lambda x,y: print_('\033[32m', x, y)
    warning = lambda x,y: print_('\033[93m', x, y)
    info = lambda x,y: print_('\033[36m', x, y)
    debug = lambda x,y: None


def print_banner():
    print("""
 ______     __  __     ______    
/\  ___\   /\ \_\ \   /\  __ \    Crack Hashes Online
\ \ \____  \ \  __ \  \ \ \/\ \   
 \ \_____\  \ \_\ \_\  \ \_____\  Filippo Lauria
  \/_____/   \/_/\/_/   \/_____/ 
    """)



def module_configuration_check(module_name, imported_module, config):
    if not hasattr(imported_module, 'do_request'):
        return {
            'success': False,
            'message': "do_request is a mandatory function"
        }
    
    if hasattr(imported_module, 'do_check_configuration'):
        return imported_module.do_check_configuration(config)
        
    return {
        'success': True,
        'message': "this module seems to be well configured"
    }


def load_modules(config):
    global max_key_len
    loaded = 0
    loadable = 0
    for module in os.listdir(path="./modules"):
        m = re.search(r'^(\w+)\.py$', module)
        if not m:
            
            continue

        module_name = m.group(1)
        module_fullname = "modules.{}".format(module_name)
        imported_module = import_module(module_fullname)

        # load verbose name
        if not hasattr(imported_module, 'verbose_name') or not imported_module.verbose_name:
            colorprint.debug(module_name,
                "using filename as module name. (verbose_name undefined/invalid?)")
            verbose_name = module_name
            imported_module.verbose_name = module_name
        else:
            verbose_name = imported_module.verbose_name

        result = module_configuration_check(
            module_name, imported_module, config)
        loadable += 1
        
        if not result['success']:
            colorprint.debug(verbose_name, result['message'])
            continue
        
        modules[imported_module.verbose_name] = imported_module
        max_key_len = max([ len(key) for key in modules.keys() ])
        loaded += 1
        colorprint.info(imported_module.verbose_name, result['message'])

    return { 
        'loadable_modules': loadable, 
        'loaded_modules': loaded, 
    }


def main(args):
    global max_key_len
    cho_name = os.path.splitext(os.path.basename(__file__))[0]
    max_key_len = len(cho_name)
    
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count',
        help="verbosity level: minimum -v, maximum -vvv")
    parser.add_argument('--stop-when-found', '-s', default=False,
        action='store_true', help="stops on the first match")
    parser.add_argument('hash', type=hash_validate,
        help="non-salted hash (only hex-digits allowed)")
    args = parser.parse_args()
    
    if not args.verbose:
        colorprint.warning = lambda x,y: None
        colorprint.info = lambda x,y: None
    elif args.verbose == 1:
        colorprint.info = lambda x,y: None
    elif args.verbose > 2:
        colorprint.debug = lambda x,y: print_('\033[34m', x, y)
    
    # ~ parse configurations
    config = configparser.ConfigParser()
    config.read('cho.user.conf')
    
    loading_result = load_modules(config)
    max_key_len = max([ len(key) for key in modules.keys() ])
    
    if loading_result['loaded_modules'] == 0:
        colorprint.failure(cho_name, "no modules could be loaded.")
        return 1

    colorp = colorprint.info if loading_result['loaded_modules'] == loading_result['loadable_modules'] else colorprint.warning

    colorp(cho_name, "loaded {} module(s) out of {}.".format(
        loading_result['loaded_modules'], loading_result['loadable_modules']
    ))

    found = False
    for name, module in modules.items():
        
        try:
            response = module.do_request(args.hash) 
            
            
            if not response['success']:
                colorprint.info(module.verbose_name,
                    "hash '{}' => unable to crack".format(args.hash))
                continue
            
            result = response['result']
            colorprint.success(module.verbose_name,
                "hash '{}' => plaintext: '{}', algorithm: '{}'".format(
                    args.hash, result['plaintext'], result['algorithm'], ))
            found = True
            
            if args.stop_when_found:
                break
                
        except:
            colorprint.failure(module.verbose_name,
                "an unknown error occurred.")

    if not found:
        colorprint.failure(cho_name,
            "none of your {} module(s) managed to crack this hash".format(
                loading_result['loaded_modules']))
    else:
        colorprint.success(cho_name, "hash successfully cracked!")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
