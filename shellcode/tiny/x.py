from pwn import *
import time

context.terminal = ['tmux', 'splitw', '-h']

r = process("./tiny")
gdb.attach(r,'''
        b puts
        c
        ''')
#gdb.attach(r)
input("wait")


r.send(b"\x90\x90\x90\x90\x90\x90\x90\x90")

r.interactive()