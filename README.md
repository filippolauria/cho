```sh
 ______     __  __     ______    
/\  ___\   /\ \_\ \   /\  __ \    Crack Hashes Online
\ \ \____  \ \  __ \  \ \ \/\ \   
 \ \_____\  \ \_\ \_\  \ \_____\  Filippo Lauria
  \/_____/   \/_/\/_/   \/_____/ 
```

**CHO** is a simple script for cracking non-salted hashes leveraging online repositories.

**Installation (for Debian/Ubuntu)**
```sh
$ sudo apt install python3 python3-pip
$ sudo pip3 install requests
$ git clone https://github.com/filippolauria/cho.git
```
Usage
-----
The basic usage is `./cho.py <hash>`

**Arguments**

CHO arguments are pretty self-explanatory:

```sh
usage: cho.py [-h] [--verbose] [--stop-when-found] hash

positional arguments:
  hash                  non-salted hash (only hex-digits allowed)

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         verbosity level: minimum -v, maximum -vvv
  --stop-when-found, -s
                        stops on the first match
```

Implemented modules
-------------------
Right now **5** modules have been implemented:
- **Hash Toolkit Module**: Hash Toolkit Hash Decrypter enables you to decrypt / reverse a hash in various formats into their original text. Find out more on [hashtoolkit.com](https://hashtoolkit.com/);
- **Hashes.org Module**: Hashes.org is a free online hash resolving service incorporating many unparalleled techniques. It is obvious that legacy methods of hash cracking are both time consuming and wasteful of resources... Find out more on [Hashes.org](https://hashes.org/);
- **NITRXGEN Module**: NITRXGEN has a look-up tool for typical unsalted MD5 cryptographic hashes. The database currently contains **1.1+ trillion passwords**. Find out more on [NITRXGEN.net](https://www.nitrxgen.net/);
- **MD5.My-Addr.com Module**: MD5.My-Addr.com is the Biggest MD5 database of Internet, size **about 4,700,000,000 hashes**. Find out more on [MD5.My-Addr.com](http://md5.my-addr.com);
- **Md5() Encrypt Module**: Md5() Encrypt & Decrypt. Find out more on [md5decrypt.net](https://md5decrypt.net/).

On the one hand, most these modules are already usable, leveraging some Regular Expressions to parse HTTP output from the contacted services. On the other hand, some modules (e.g. Hashes.org Module, etc.) require further configuration parameters, which can be submitted to CHO through the configuration file `cho.user.conf`.


How does it work? (programmer side)
-----------------------------------
CHO is a single threaded tool (multithreading capabilities have not been used), which has a modular structure. Each module has two mandatory `attr`:
- `do_request(h)`: this is the core function of a module, which is responsible for querying (online?) hash databases, starting from a string (`h`).
- `verbose_name`: this is a string variable representing the module unique name.

and an optional function `do_check_configuration(config)`, which performs some other checks starting from a ConfigParser object (`config`).

Examples
--------
```sh
$ echo -n "11111111" | md5sum | cut -d' ' -f1
1bbd886460827015e5d605ed44252251
$ ./cho.py -s 1bbd886460827015e5d605ed44252251
  ...
       NITRXGEN: hash '1bbd886460827015e5d605ed44252251' => plaintext: '11111111', algorithm: 'md5'
            cho: hash successfully cracked!
```

```sh
$ ./cho.py -vvv $( echo -n "141830982" | md5sum | cut -d' ' -f1 )
  ...
MD5.My-Addr.com: this module seems to be well configured
     Hashes.org: have you configured API Key?
  Md5() Decrypt: this module seems to be well configured
       NITRXGEN: this module seems to be well configured
   Hash Toolkit: this module seems to be well configured
            cho: loaded 4 module(s) out of 5.
  Md5() Decrypt: hash '7a5c2392d26b8e656edecb81200cfbbe' => unable to crack
       NITRXGEN: hash '7a5c2392d26b8e656edecb81200cfbbe' => plaintext: '141830982', algorithm: 'md5'
   Hash Toolkit: hash '7a5c2392d26b8e656edecb81200cfbbe' => unable to crack
MD5.My-Addr.com: hash '7a5c2392d26b8e656edecb81200cfbbe' => plaintext: '141830982', algorithm: 'md5'
            cho: hash successfully cracked!
```

```sh
$ ./cho.py -vv $( echo -n "thestrongestmd5hashintheworld" | md5sum | cut -d' ' -f1 )
  ...   
MD5.My-Addr.com: this module seems to be well configured
  Md5() Decrypt: this module seems to be well configured
       NITRXGEN: this module seems to be well configured
   Hash Toolkit: this module seems to be well configured
            cho: loaded 4 module(s) out of 5.
MD5.My-Addr.com: hash '17be2d7b5d2c9381ab451cd725cca07c' => unable to crack
       NITRXGEN: hash '17be2d7b5d2c9381ab451cd725cca07c' => unable to crack
   Hash Toolkit: hash '17be2d7b5d2c9381ab451cd725cca07c' => unable to crack
  Md5() Decrypt: hash '17be2d7b5d2c9381ab451cd725cca07c' => unable to crack
            cho: none of your 4 module(s) managed to crack this hash
```            

Contributors
------------
- Filippo Lauria (filippo[dot]lauria[at]iit[dot]cnr[dot]it)
- Gruppo Reti IIT-CNR (grupporeti[dash]dev[at]iit[dot]cnr[dot]it)
